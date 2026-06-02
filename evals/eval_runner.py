#!/usr/bin/env python3
"""
eval_runner.py — Motor de regressão para a Biblioteca de Prompts Profissionais
================================================================================
v1.1.0 (julho de 2026)

Roda um prompt versionado da biblioteca contra seu golden set, calcula métricas
de aderência por categoria (fáceis / médios / limítrofes) e bloqueia o release
quando a pontuação cair abaixo do limiar declarado.

PRINCÍPIOS APLICADOS DA OBRA
----------------------------
- F8 Pirâmide da Avaliação: base canônica + meio ambíguo + topo adversarial
- Princípio 7 Termômetro Permanente: eval contínuo, com base, meio e topo definidos
- Princípio 5 Honestidade Temporal: cada caso carrega data de calibração; cada release
  carrega changelog datado.

ARQUITETURA
-----------
Três camadas:
  1) Provedor (provider): adapter para Anthropic / OpenAI / Google / Local
  2) Avaliador (judge): heurística (substring, regex, schema), LLM-as-judge, ou ambos
  3) Reporter: console + JSON + (opcional) gate de CI

CADA EXECUÇÃO PRODUZ
--------------------
- Relatório em console, agregado e por categoria
- Arquivo JSON timestampado em ./reports/
- Exit code 0 (passou no limiar) ou 1 (falhou — gate de CI bloqueia)

USO
---
    # Roda um prompt contra seu golden set
    python eval_runner.py --prompt P-LEG-01 --provider anthropic --model claude-sonnet-4-6

    # Roda todos os prompts (suite completa)
    python eval_runner.py --suite all --provider anthropic --model claude-haiku-4-5

    # Modo dry-run (não chama o modelo, valida estrutura)
    python eval_runner.py --prompt P-LEG-01 --dry-run

    # Modo CI: falha o build se score < limiar
    python eval_runner.py --prompt P-LEG-01 --ci

CONFIGURAÇÃO
------------
Variáveis de ambiente esperadas:
  ANTHROPIC_API_KEY
  OPENAI_API_KEY
  GOOGLE_API_KEY (Gemini)

Estrutura esperada no repositório:
  prompts/{ID}/
      prompt.xml         (prompt em XML versionado, blocos do F4)
      golden.yaml        (20 casos calibrados)
      eval.config.yaml   (limiares, métricas ativas, modelo padrão)
  datasets/{ID}.jsonl    (golden set compilado em JSONL — opcional, gerado por compile_golden_sets.py)

LIMITAÇÕES CONHECIDAS
---------------------
- LLM-as-judge não é determinístico. Usar temperatura 0 e múltiplas amostras quando
  a métrica for crítica para gate de release. Calibrar contra rotulagem humana em
  marcos trimestrais conforme F8.
- Custo de execução em suite completa (30 prompts × 20 casos = 600 chamadas) pode
  passar de USD 5-15 dependendo do modelo. Configurar HAIKU como modelo padrão de CI
  e reservar Opus apenas para release final.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import pathlib
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any, Callable

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
DATASETS_DIR = ROOT / "datasets"
REPORTS_DIR = pathlib.Path(__file__).parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


# ============================================================================
# DOMÍNIO
# ============================================================================

@dataclasses.dataclass
class GoldenCase:
    """Caso individual de um golden set."""
    id: str
    category: str  # 'facil' | 'medio' | 'limitrofe'
    input: dict
    expected: dict
    calibration_date: str
    notes: str = ""


@dataclasses.dataclass
class EvalResult:
    """Resultado da avaliação de um caso individual."""
    case_id: str
    category: str
    passed: bool
    score: float  # 0.0 a 1.0
    metrics: dict
    output_raw: str
    duration_ms: int
    error: str | None = None


@dataclasses.dataclass
class SuiteReport:
    """Relatório agregado de uma execução completa de prompt."""
    prompt_id: str
    model: str
    provider: str
    started_at: str
    duration_s: float
    results: list[EvalResult]
    threshold: float
    passed: bool

    @property
    def by_category(self) -> dict[str, dict]:
        agg = {}
        for cat in ('facil', 'medio', 'limitrofe'):
            cases = [r for r in self.results if r.category == cat]
            if not cases:
                agg[cat] = {'count': 0, 'passed': 0, 'score_mean': 0.0}
                continue
            agg[cat] = {
                'count': len(cases),
                'passed': sum(1 for c in cases if c.passed),
                'score_mean': sum(c.score for c in cases) / len(cases),
            }
        return agg

    @property
    def overall_score(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.score for r in self.results) / len(self.results)


# ============================================================================
# PROVEDORES (adapters de chamada ao modelo)
# ============================================================================

class Provider:
    """Interface mínima de adapter de modelo."""
    name = "abstract"

    def call(self, prompt: str, model: str, timeout: int = 60) -> str:
        raise NotImplementedError


class AnthropicProvider(Provider):
    name = "anthropic"

    def call(self, prompt: str, model: str, timeout: int = 60) -> str:
        try:
            import anthropic
        except ImportError:
            raise RuntimeError(
                "Provedor 'anthropic' requer o pacote: pip install anthropic"
            )
        client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        msg = client.messages.create(
            model=model,
            max_tokens=4096,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout,
        )
        return msg.content[0].text


class OpenAIProvider(Provider):
    name = "openai"

    def call(self, prompt: str, model: str, timeout: int = 60) -> str:
        try:
            from openai import OpenAI
        except ImportError:
            raise RuntimeError(
                "Provedor 'openai' requer o pacote: pip install openai"
            )
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        r = client.chat.completions.create(
            model=model,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
            timeout=timeout,
        )
        return r.choices[0].message.content


class DryRunProvider(Provider):
    """Provedor que não chama API — valida estrutura."""
    name = "dry-run"

    def call(self, prompt: str, model: str, timeout: int = 60) -> str:
        # Retorna saída sintética compatível com o schema esperado
        return '{"status": "dry-run", "schema_valid": true}'


PROVIDERS = {
    "anthropic": AnthropicProvider,
    "openai": OpenAIProvider,
    "dry-run": DryRunProvider,
}


# ============================================================================
# AVALIADORES (judges)
# ============================================================================

def judge_substring(output: str, expected: dict) -> tuple[bool, float, dict]:
    """Verifica presença de substrings obrigatórias no output."""
    required = expected.get("must_contain", [])
    forbidden = expected.get("must_not_contain", [])
    hit_req = sum(1 for s in required if s.lower() in output.lower())
    hit_forb = sum(1 for s in forbidden if s.lower() in output.lower())
    score_req = hit_req / max(len(required), 1)
    score_forb = 1.0 if hit_forb == 0 else 0.0
    score = (score_req + score_forb) / 2
    return score >= 0.8, score, {
        "required_hit": f"{hit_req}/{len(required)}",
        "forbidden_hit": hit_forb,
    }


def judge_regex(output: str, expected: dict) -> tuple[bool, float, dict]:
    """Verifica padrões regex obrigatórios e proibidos."""
    required = expected.get("regex_required", [])
    forbidden = expected.get("regex_forbidden", [])
    hit_req = sum(1 for p in required if re.search(p, output, re.IGNORECASE | re.DOTALL))
    hit_forb = sum(1 for p in forbidden if re.search(p, output, re.IGNORECASE | re.DOTALL))
    score_req = hit_req / max(len(required), 1)
    score_forb = 1.0 if hit_forb == 0 else 0.0
    score = (score_req + score_forb) / 2
    return score >= 0.8, score, {
        "regex_hit": f"{hit_req}/{len(required)}",
        "regex_forbidden_hit": hit_forb,
    }


def judge_json_schema(output: str, expected: dict) -> tuple[bool, float, dict]:
    """Valida que o output é JSON parseável com chaves esperadas."""
    keys = expected.get("json_keys", [])
    try:
        # Tenta extrair JSON de qualquer lugar do output
        m = re.search(r'\{.*\}', output, re.DOTALL)
        if not m:
            return False, 0.0, {"json_parse": "no JSON found"}
        data = json.loads(m.group(0))
        hit = sum(1 for k in keys if k in data)
        score = hit / max(len(keys), 1)
        return score >= 0.9, score, {
            "json_keys_hit": f"{hit}/{len(keys)}",
            "json_valid": True,
        }
    except json.JSONDecodeError as e:
        return False, 0.0, {"json_parse": str(e)}


def judge_classification(output: str, expected: dict) -> tuple[bool, float, dict]:
    """Compara classificação categórica esperada."""
    expected_class = expected.get("classification")
    if not expected_class:
        return True, 1.0, {}
    # Procura a classificação no output
    found = expected_class.lower() in output.lower()
    return found, 1.0 if found else 0.0, {
        "expected_class": expected_class,
        "found": found,
    }


JUDGES: dict[str, Callable] = {
    "substring": judge_substring,
    "regex": judge_regex,
    "json_schema": judge_json_schema,
    "classification": judge_classification,
}


# ============================================================================
# CARREGADORES
# ============================================================================

def load_golden_set(prompt_id: str) -> list[GoldenCase]:
    """Carrega golden set de um prompt — YAML em prompts/{ID}/golden.yaml
    ou JSONL em datasets/{ID}.jsonl (preferido em CI)."""
    jsonl_path = DATASETS_DIR / f"{prompt_id}.jsonl"
    yaml_path = PROMPTS_DIR / prompt_id / "golden.yaml"

    cases = []
    if jsonl_path.exists():
        for line in jsonl_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            d = json.loads(line)
            cases.append(GoldenCase(
                id=d["id"],
                category=d["category"],
                input=d["input"],
                expected=d["expected"],
                calibration_date=d.get("calibration_date", ""),
                notes=d.get("notes", ""),
            ))
    elif yaml_path.exists():
        try:
            import yaml
        except ImportError:
            raise RuntimeError("Carregar YAML requer: pip install pyyaml")
        data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        for c in data.get("cases", []):
            cases.append(GoldenCase(
                id=c["id"],
                category=c["category"],
                input=c["input"],
                expected=c["expected"],
                calibration_date=c.get("calibration_date", ""),
                notes=c.get("notes", ""),
            ))
    else:
        raise FileNotFoundError(
            f"Golden set não encontrado para {prompt_id} "
            f"(procurado em {jsonl_path} e {yaml_path})"
        )
    return cases


def load_prompt(prompt_id: str) -> str:
    """Carrega o XML do prompt."""
    path = PROMPTS_DIR / prompt_id / "prompt.xml"
    if not path.exists():
        raise FileNotFoundError(f"Prompt não encontrado: {path}")
    return path.read_text(encoding="utf-8")


def load_config(prompt_id: str) -> dict:
    """Carrega eval.config.yaml — limiar, judges ativos, modelo padrão."""
    path = PROMPTS_DIR / prompt_id / "eval.config.yaml"
    defaults = {
        "threshold": 0.85,
        "judges": ["substring", "regex", "json_schema"],
        "model_default": "claude-haiku-4-5",
        "provider_default": "anthropic",
    }
    if not path.exists():
        return defaults
    try:
        import yaml
    except ImportError:
        return defaults
    cfg = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {**defaults, **cfg}


# ============================================================================
# EXECUÇÃO
# ============================================================================

def render_prompt(prompt_xml: str, case_input: dict) -> str:
    """Substitui variáveis {{var}} no prompt pelos valores do caso."""
    rendered = prompt_xml
    for k, v in case_input.items():
        rendered = rendered.replace(f"{{{{{k}}}}}", str(v))
    return rendered


def evaluate_case(
    prompt_xml: str,
    case: GoldenCase,
    provider: Provider,
    model: str,
    judges_active: list[str],
) -> EvalResult:
    """Executa um caso individual e devolve resultado consolidado."""
    rendered = render_prompt(prompt_xml, case.input)
    t0 = time.time()
    try:
        output = provider.call(rendered, model=model)
    except Exception as e:
        return EvalResult(
            case_id=case.id,
            category=case.category,
            passed=False,
            score=0.0,
            metrics={},
            output_raw="",
            duration_ms=int((time.time() - t0) * 1000),
            error=str(e),
        )

    scores = []
    metrics_combined = {}
    for j in judges_active:
        if j not in JUDGES:
            continue
        passed_j, score_j, metrics_j = JUDGES[j](output, case.expected)
        scores.append(score_j)
        metrics_combined[j] = {"passed": passed_j, "score": score_j, **metrics_j}

    score = sum(scores) / len(scores) if scores else 0.0
    passed = score >= 0.8

    return EvalResult(
        case_id=case.id,
        category=case.category,
        passed=passed,
        score=score,
        metrics=metrics_combined,
        output_raw=output[:2000],  # truncar para o relatório
        duration_ms=int((time.time() - t0) * 1000),
    )


def run_suite(prompt_id: str, provider_name: str, model: str | None,
              dry_run: bool = False) -> SuiteReport:
    config = load_config(prompt_id)
    if dry_run:
        provider_name = "dry-run"
    elif not provider_name:
        provider_name = config["provider_default"]
    model = model or config["model_default"]
    threshold = config["threshold"]
    judges_active = config["judges"]

    provider = PROVIDERS[provider_name]()
    prompt_xml = load_prompt(prompt_id)
    cases = load_golden_set(prompt_id)

    started = time.time()
    results = []
    for c in cases:
        r = evaluate_case(prompt_xml, c, provider, model, judges_active)
        results.append(r)

    duration = time.time() - started
    report = SuiteReport(
        prompt_id=prompt_id,
        model=model,
        provider=provider_name,
        started_at=datetime.fromtimestamp(started, timezone.utc).isoformat(),
        duration_s=duration,
        results=results,
        threshold=threshold,
        passed=False,  # define abaixo
    )
    report.passed = report.overall_score >= threshold
    return report


# ============================================================================
# REPORTING
# ============================================================================

def print_report(report: SuiteReport) -> None:
    print()
    print("=" * 72)
    print(f"  PROMPT: {report.prompt_id}")
    print(f"  MODELO: {report.model} ({report.provider})")
    print(f"  INÍCIO: {report.started_at}")
    print(f"  TEMPO:  {report.duration_s:.1f}s")
    print("=" * 72)
    print()
    print(f"Casos executados: {len(report.results)}")
    print(f"Score geral:      {report.overall_score:.3f}")
    print(f"Limiar:           {report.threshold:.3f}")
    print(f"Resultado:        {'✓ PASSOU' if report.passed else '✗ FALHOU'}")
    print()
    print("Por categoria:")
    for cat, agg in report.by_category.items():
        if agg['count'] == 0:
            continue
        print(f"  {cat:11s}  {agg['passed']:2d}/{agg['count']:2d} casos  "
              f"score médio {agg['score_mean']:.3f}")
    print()
    falhas = [r for r in report.results if not r.passed]
    if falhas:
        print(f"Casos com falha ({len(falhas)}):")
        for f in falhas[:10]:
            print(f"  - {f.case_id} ({f.category}) score {f.score:.2f}")
            if f.error:
                print(f"      erro: {f.error}")


def write_json_report(report: SuiteReport) -> pathlib.Path:
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = REPORTS_DIR / f"{report.prompt_id}_{ts}.json"
    data = {
        "prompt_id": report.prompt_id,
        "model": report.model,
        "provider": report.provider,
        "started_at": report.started_at,
        "duration_s": report.duration_s,
        "threshold": report.threshold,
        "passed": report.passed,
        "overall_score": report.overall_score,
        "by_category": report.by_category,
        "results": [dataclasses.asdict(r) for r in report.results],
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


# ============================================================================
# CLI
# ============================================================================

def cmd_one(args):
    report = run_suite(
        prompt_id=args.prompt,
        provider_name=args.provider,
        model=args.model,
        dry_run=args.dry_run,
    )
    print_report(report)
    out = write_json_report(report)
    print(f"\nRelatório salvo em {out}")
    if args.ci and not report.passed:
        sys.exit(1)


def cmd_suite(args):
    if args.suite == "all":
        prompts = sorted([p.name for p in PROMPTS_DIR.iterdir() if p.is_dir()])
    else:
        prompts = args.suite.split(",")

    all_passed = True
    for pid in prompts:
        print(f"\n>>> Rodando {pid}...")
        try:
            report = run_suite(pid, args.provider, args.model, args.dry_run)
            print_report(report)
            write_json_report(report)
            if not report.passed:
                all_passed = False
        except Exception as e:
            print(f"  ERRO em {pid}: {e}")
            all_passed = False

    if args.ci and not all_passed:
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser(
        description="Motor de regressão da Biblioteca de Prompts Profissionais",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("--prompt", help="ID do prompt (ex: P-LEG-01)")
    ap.add_argument("--suite", help="Lista de prompts ou 'all'")
    ap.add_argument("--provider", default="anthropic",
                    choices=list(PROVIDERS.keys()))
    ap.add_argument("--model", help="Modelo específico (sobrescreve config)")
    ap.add_argument("--dry-run", action="store_true",
                    help="Não chama API — valida estrutura")
    ap.add_argument("--ci", action="store_true",
                    help="Exit 1 se score < limiar (gate de CI)")

    args = ap.parse_args()
    if args.prompt:
        cmd_one(args)
    elif args.suite:
        cmd_suite(args)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
