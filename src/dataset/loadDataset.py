from enum import Enum
import json
from pathlib import Path
from typing import List
from pydantic import BaseModel
import numpy as np
from src.config.config import Config
from src.config.config import LoadConfig
class EVFormat(BaseModel):
    x: int
    y: int
    t: float
    p: int
    label: int
    name: int


class EVSNORMFormat(BaseModel):
    x: float
    y: float
    t: float
    p: int 
    label: int 
    name: int

class EVLOCFormat(BaseModel):
    x: int
    y: int
    t: float
    
    
    
class DataWithName(BaseModel):
    name: str
    data: List[EVFormat]

class DataMode(Enum):
    train = 1
    test = 2
    val = 3
class DataLoader:
    """
    读取对应的.npz数据
    你所需要使用的接口:
        init 填入cfg和需要训练的模式"train","test","val"
        load_npz_file() 没有参数
    有意义的参数:
        self.cfg 配置的config
        self.nparray 读取的numpy数组
    """
    def __init__(self ,cfg : Config,datamode: DataMode) ->None:
        self._config = cfg
        self._datamode = datamode
        self.nparray = []
        
        
    ###
    def __chosen_mode(self):
        if self._datamode == DataMode.train:
            self._npz_root_path = self._config.dataset[0].path_root
        elif self._datamode == DataMode.test:
             self._npz_root_path = self._config.dataset[1].path_root
        elif self._datamode == DataMode.val:
            self._npz_root_path = self._config.dataset[2].path_root
        else:
            raise "panic,TODO"
    ####
    
    def __read_the_npz(self):
        floader = Path(self._npz_root_path)
        self._npz_file = [file for file in floader.glob("**/*.npz")]
    
    ###
    def load_npz_file(self):
        """
        载入.npz文件
        """
        self.__chosen_mode()
        self.__read_the_npz()
        self.__load_to_numpy()
        
    '''
    让对应nparray转化为json文件
    '''
    def to_json(self,output_root_path : str = "./tmp/json"):
        print(f"totol line is {len(self.nparray)}")
        for i in range(len(self.nparray)):
            evs = self.__parse_ev__(i)
            ev_norms =self.__parse_ev_norm__(i)
            ev_locs = self.__parse_ev_loc__(i)
            dict_ev = [ev.model_dump() for ev in evs]
            dict_ev_norms = [ev_norm.model_dump() for ev_norm in ev_norms]
            dict_ev_loc = [ev_loc.model_dump() for ev_loc in ev_locs]
            json_ev = json.dumps(dict_ev , indent= 2)
            json_ev_norm = json.dumps(dict_ev_norms,indent=2)
            json_ev_loc = json.dumps(dict_ev_loc,indent=2)
            with open("./tmp/json/ev/" + "ev" + str(i) + ".json","a",encoding="utf-8") as f:
                f.write(json_ev)
            with open("./tmp/json/ev_norm/" + "ev_norm" + str(i) + ".json","a",encoding="utf-8") as f:
                f.write(json_ev_norm)
            with open("./tmp/json/ev_loc/" + "ev_loc" + str(i) + ".json","a",encoding="utf-8") as f:
                f.write(json_ev_loc)
            
    def __load_to_numpy(self):
        for _ , file in enumerate(self._npz_file):
            self.nparray.append(np.load(file))
    
    
    #####
    def __parse_ev__(self,i : int) -> List[EVFormat]:
        res = []
        ev_np = self.nparray[i]
        evs = ev_np["ev"]
        for ev in evs:
            (x,y,t,p,label,name) = ev
            res.append(EVFormat(x=x,y=y,t=t,p=p,label=label,name=name))
        return res            
    def __parse_ev_norm__(self,i : int) -> List[EVSNORMFormat]:
        res = []
        ev_np = self.nparray[i]
        evs = ev_np["evs_norm"]
        for ev in evs:
            (x,y,t,p,label,name) = ev
            res.append(EVSNORMFormat(x=x,y=y,t=t,p=p,label=label,name=name))
        return res
    def __parse_ev_loc__(self,i : int) -> List[EVLOCFormat]:
        res = []
        ev_np = self.nparray[i]
        evs = ev_np["ev_loc"]
        for ev in evs:
            (x,y,t) = ev
            res.append(EVLOCFormat(x=x,y=y,t=t))
        return res
    
    ###
            
            
    def __repr__(self) -> str:
        s = f"config is {self._config}\n"
        s += f"datamode is {self._datamode}\n"
        for f in self._npz_file:
            s += f"npz file is {f}\n"
        s += f"nparray is {self.nparray}"
        return s  
    
if __name__ == "__main__":
    cfg = LoadConfig()
    dataLoader = DataLoader(cfg,DataMode.train)
    dataLoader.load_npz_file()
    dataLoader.to_json()
    
    ##print(dataLoader)         
        
        
    
    