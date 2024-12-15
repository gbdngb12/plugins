from typing import Optional, List
import subprocess
import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Workspace:
    id: int
    name: str

@dataclass
class HyprlandClient:
    address: str
    # mapped: bool
    # hidden: bool
    # at: List[int]
    # size: List[int]
    workspace: Workspace
    # floating: bool
    # pseudo: bool
    monitor: int
    window_class: str  # "class" 필드는 예약어이므로 변경
    title: str
    # initialClass: str
    # initialTitle: str
    # pid: int
    # xwayland: bool
    # pinned: bool
    # fullscreen: int
    # fullscreenClient: int
    # grouped: List[str]
    # tags: List[str]
    # swallowing: str
    # focusHistoryID: int

    @classmethod
    def from_dict(cls, data: dict):
        # workspace를 먼저 처리
        ws_data = data.get("workspace", {})
        workspace = Workspace(id=ws_data["id"], name=ws_data["name"])

        # HyprlandClient 인스턴스 생성
        return cls(
            address=data["address"],
            # mapped=data["mapped"],
            # hidden=data["hidden"],
            # at=data["at"],
            # size=data["size"],
            workspace=workspace,
            # floating=data["floating"],
            # pseudo=data["pseudo"],
            monitor=data["monitor"],
            window_class=data["class"],
            title=data["title"],
            # initialClass=data["initialClass"],
            # initialTitle=data["initialTitle"],
            # pid=data["pid"],
            # xwayland=data["xwayland"],
            # pinned=data["pinned"],
            # fullscreen=data["fullscreen"],
            # fullscreenClient=data["fullscreenClient"],
            # grouped=data["grouped"],
            # tags=data["tags"],
            # swallowing=data["swallowing"],
            # focusHistoryID=data["focusHistoryID"]
        )

class HyprlandWindowManager:
    def __init__(self):
        pass
    def _run_command(self, command:str) -> Optional[str]:
        try:
            result = subprocess.run(
                command, capture_output=True, shell=True, text=True
            )
            print(f"command : {command}")
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Command failed: {command}")
            print(f"Error output: {e.stderr}")
            return None
    def get_current_windows(self) -> Optional[List[HyprlandClient]]:
        results:List[HyprlandClient] = []
        hyprland_client_jsons = self._run_command("hyprctl -j clients")
        if hyprland_client_jsons is None:
            return None
        hyprland_client_jsons = json.loads(hyprland_client_jsons)
        for hyprland_client in hyprland_client_jsons:
            results.append(HyprlandClient(hyprland_client["address"],Workspace(hyprland_client["workspace"]["id"], hyprland_client["workspace"]["name"]),hyprland_client["monitor"], hyprland_client["class"],hyprland_client["title"]))
        return results
    def switch_window(self, address:str):
        # hyprctl dispatch focuswindow address:0x6083e13d8620
        ret = self._run_command(f"hyprctl dispatch focuswindow address:{address}")
        

hypr = HyprlandWindowManager()
target = "0x6083e13d8620"
for r in hypr.get_current_windows():
    print(r.address)
    print(r.title)

hypr.switch_window(target)
