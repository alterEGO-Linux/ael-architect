from __future__ import annotations
from pathlib import Path
from flask import Flask,jsonify,render_template,request
from ael_architect.addons import AddonManager
from ael_architect.config import ConfigManager

def create_app(config_path:Path):
    app=Flask(__name__)
    cm=ConfigManager(config_path)
    manager=AddonManager(cm)
    manager.packages.sync_actual_state()
    startup_results=manager.reconcile_all()

    @app.get("/")
    def index():
        addons = [
            report
            for report in manager.reports()
            if report.visible
        ]

        packages = [
            report
            for report in manager.packages.reports()
            if report.visible
        ]

        return render_template(
            "index.html",
            addons=addons,
            packages=packages,
            config_path=config_path,
            startup_results=startup_results,
        )

    @app.post("/api/addons/<name>/check")
    def check_addon(name):
        checks,state=manager.check(name); return jsonify(success=True,state=state,checks=[{"name":c.name,"ok":c.ok,"detail":c.detail} for c in checks])
    @app.post("/api/addons/<name>/set-enabled")
    def set_addon(name):
        result=manager.set_enabled(name,bool(request.json.get("enabled",False))); r=manager.get(name); return jsonify(success=result.success,message=result.message,enabled=r.enabled,state=r.state)
    @app.post("/api/packages/<name>/check")
    def check_package(name):
        checks,state=manager.packages.health_check(name); return jsonify(success=True,state=state,checks=[{"name":c.name,"ok":c.ok,"detail":c.detail} for c in checks])
    @app.post("/api/packages/<name>/set-enabled")
    def set_package(name):
        result=manager.packages.set_enabled(name,bool(request.json.get("enabled",False))); r=manager.packages.report(name); return jsonify(success=result.success,message=result.message,enabled=r.enabled,state=r.state)
    return app
