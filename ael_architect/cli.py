from __future__ import annotations
import argparse
from pathlib import Path
from ael_architect.addons import AddonManager
from ael_architect.config import ConfigManager

def build_parser():
    p=argparse.ArgumentParser(prog="ael-architect"); p.add_argument("-c","--config",default="alterego.toml"); p.add_argument("--apply",action="store_true"); sub=p.add_subparsers(dest="command"); sub.add_parser("status"); sub.add_parser("tui"); web=sub.add_parser("web"); web.add_argument("--host",default="127.0.0.1"); web.add_argument("--port",type=int,default=5000); web.add_argument("--debug",action="store_true"); return p

def main():
    args=build_parser().parse_args(); config=ConfigManager(args.config); manager=AddonManager(config)
    if args.command=="tui":
        from ael_architect.tui import ArchitectApp; ArchitectApp(Path(args.config)).run(); return
    if args.command=="web":
        from ael_architect.web import create_app; create_app(Path(args.config)).run(host=args.host,port=args.port,debug=args.debug); return
    if args.apply:
        results=manager.reconcile_all();
        if not results: print("Nothing to apply.")
        for name,result in results.items(): print(f"{name}: {'OK' if result.success else 'FAILED'}\n  {result.message}")
        return
    print("Add-ons")
    for r in manager.reports(): print(f"  {r.name}: enabled={str(r.enabled).lower()} state={r.state}")
    print("Packages")
    for r in manager.packages.reports(): print(f"  {r.key}: enabled={str(r.enabled).lower()} state={r.state}")

if __name__=="__main__": main()
