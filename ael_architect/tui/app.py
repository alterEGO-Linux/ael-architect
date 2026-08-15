from __future__ import annotations
from pathlib import Path
from textual import work
from textual.app import App,ComposeResult
from textual.containers import Horizontal,Vertical,VerticalScroll
from textual.widgets import Button,Footer,Header,Label,RichLog,Static,Switch
from ael_architect.addons import AddonManager
from ael_architect.config import ConfigManager

class ItemRow(Horizontal):
    def __init__(self,key,display_name,description,enabled,prefix): super().__init__(classes="item-row"); self.key=key; self.display_name=display_name; self.description=description; self.enabled=enabled; self.prefix=prefix
    def compose(self):
        with Vertical(classes="item-info"):
            yield Label(self.display_name,classes="item-display_name"); yield Static(self.description,classes="item-description")
        yield Button("Check",id=f"{self.prefix}-check--{self.key}",classes="check-button")
        yield Switch(value=self.enabled,id=f"{self.prefix}-switch--{self.key}",classes="item-switch")

class ArchitectApp(App):
    TITLE="AlterEGO Architect"
    CSS="#workspace{height:1fr} #sidebar{width:20;border-right:solid $primary;background:$panel;padding-top:1}.category{width:100%;height:2;border:none;margin:0}.category-active{background:$primary;text-style:bold}#main{width:1fr;padding:0 2}#section-title{height:3;padding-top:1;text-style:bold}#addons-list,#packages-list{height:1fr;padding-top:1}#packages-list{display:none}.item-row{height:5;border:round $primary;padding:0 1;margin-bottom:1;align:center middle}.item-info{width:1fr;height:3;padding-right:2}.item-display_name{height:1;text-style:bold}.item-description{height:2;color:$text-muted}.check-button{width:12;height:3;margin-right:2}.item-switch{width:8;margin-right:1}#message{height:8;border:round $accent;padding:0 1;margin-bottom:1}"

    def __init__(self,config_path:Path):
        super().__init__()

        self.config_manager=ConfigManager(config_path)
        self.manager=AddonManager(self.config_manager)

        # --- Synchronize packages with what is actually installed before
        # ... Textual creates the package switches.
        self.manager.packages.sync_actual_state()

        self.ignore_switch=False

    def compose(self):
        yield Header()
        with Horizontal(id="workspace"):
            with Vertical(id="sidebar"):
                for display_name in ["System","Desktop","Add-ons","Packages","Services"]: yield Button(display_name,id=f"category--{display_name.lower().replace(' ','-')}",classes="category"+(" category-active" if display_name=="Add-ons" else ""))
            with Vertical(id="main"):
                yield Static("Add-ons",id="section-title")
                with VerticalScroll(id="addons-list"):
                    for r in self.manager.reports():
                        if r.visible:
                            yield ItemRow(
                                r.name,
                                r.name,
                                r.description,
                                r.enabled,
                                "addon"
                            )
                with VerticalScroll(id="packages-list"):
                    for r in self.manager.packages.reports():
                        if r.visible:
                            yield ItemRow(
                                r.key,
                                r.name,
                                f"{r.description} [{r.source}]",
                                r.enabled,
                                "package"
                            )
                yield Static("Result"); yield RichLog(id="message",markup=True,wrap=True)
        yield Footer()
    def on_mount(self): self.apply_startup()
    def show_message(self,msg):
        log=self.query_one("#message",RichLog); log.clear(); [log.write(line) for line in msg.splitlines()]
    @work(thread=True,exclusive=True)
    def apply_startup(self):
        results=self.manager.reconcile_all(); lines=["[bold]Startup apply[/bold]"]+[f"{'✓' if r.success else '✗'} {n}: {r.message}" for n,r in results.items()]; self.call_from_thread(self.show_message,"\n".join(lines if len(lines)>1 else lines+["Nothing to do."]))
    def on_button_pressed(self,event):
        bid=event.button.id or ""
        if bid.startswith("category--"):
            cat=bid.removeprefix("category--"); addons=self.query_one("#addons-list"); packages=self.query_one("#packages-list"); addons.styles.display="block" if cat=="add-ons" else "none"; packages.styles.display="block" if cat=="packages" else "none"; self.query_one("#section-title",Static).update("Packages" if cat=="packages" else "Add-ons" if cat=="add-ons" else cat.title()); return
        if bid.startswith("addon-check--"): self.check_addon(bid.removeprefix("addon-check--"))
        elif bid.startswith("package-check--"): self.check_package(bid.removeprefix("package-check--"))
    def on_switch_changed(self,event):
        if self.ignore_switch:return
        sid=event.switch.id or ""
        if sid.startswith("addon-switch--"): self.set_addon(sid.removeprefix("addon-switch--"),event.value)
        elif sid.startswith("package-switch--"): self.set_package(sid.removeprefix("package-switch--"),event.value)
    @work(thread=True,exclusive=True)
    def check_addon(self,name):
        checks,state=self.manager.check(name); self.call_from_thread(self.show_message,"\n".join([f"{name}: state={state}"]+[f"{'✓' if c.ok else '✗'} {c.name}: {c.detail}" for c in checks]))
    @work(thread=True,exclusive=True)
    def check_package(self,name):
        checks,state=self.manager.packages.health_check(name); self.call_from_thread(self.show_message,"\n".join([f"{name}: state={state}"]+[f"{'✓' if c.ok else '✗'} {c.name}: {c.detail}" for c in checks]))
    @work(thread=True,exclusive=True)
    def set_addon(self,name,enabled): self.call_from_thread(self.show_message,self.manager.set_enabled(name,enabled).message)
    @work(thread=True,exclusive=True)
    def set_package(self,name,enabled): self.call_from_thread(self.show_message,self.manager.packages.set_enabled(name,enabled).message)
