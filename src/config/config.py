from typing import List
from pydantic import BaseModel
import yaml
###数据集的配置
class DataSetConfig(BaseModel):
    name: str
    path_root: str
    
###所有的配置
class Config(BaseModel):
    module: str
    version: str
    description: str
    dataset : List[DataSetConfig]
    
###配置文件路径
pathOfConfig = "./src/config/config.yaml"

###载入文件
def LoadConfig(configPath : str = pathOfConfig) -> Config:
    """_summary_

    Args:
        configPath (str, optional): _description_. Defaults to pathOfConfig.
        configPath 默认的读取参数config.yaml的路径,有需求可以修改
    Returns:
        Config: 读取的config结构体
    """
    with open(pathOfConfig,'r',encoding='UTF-8') as f:
        yaml_data = yaml.safe_load(f)
        config = Config(**yaml_data)
        return config
### 
    
if __name__ == "__main__":
    cfg = LoadConfig()
    print(f"read config is {cfg}")
    