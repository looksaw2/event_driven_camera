<# 定义各个功能函数 #>
function Invoke-Init {
    Write-Host "开始安装uv(失败请手动安装)"
    try {
        (Invoke-WebRequest -Uri https://astral.sh/uv/install.sh -UseBasicParsing).Content | sh
        Write-Host "安装uv成功"
        
        Write-Host "启动虚拟环境"
        uv init
        uv venv
        Write-Host "启动虚拟环境成功"
        
        Write-Host "同步依赖"
        uv sync
        Write-Host "同步虚拟环境成功"
    }
    catch {
        Write-Error "执行init过程中出错: $_"
        exit 1
    }
}

function Invoke-ShowConfig {
    try {
        Write-Host "start to run the config.py file"
        python -m src.config.config
        Write-Host "Finish ..........................."
    }
    catch {
        Write-Error "执行showConfig过程中出错: $_"
        exit 1
    }
}

function Invoke-RunDataset {
    try {
        Write-Host "start to show the loaddataset.py file"
        python -m src.dataset.loadDataset
        Write-Host "Finish.........................."
    }
    catch {
        Write-Error "执行runDataset过程中出错: $_"
        exit 1
    }
}

function Invoke-ShowData {
    try {
        Write-Host "开始展示数据可视化"
        uv run ./src/visualization/plot.py
        Write-Host "结束，已保存./tmp/img当中请用浏览器打开"
    }
    catch {
        Write-Error "执行showData过程中出错: $_"
        exit 1
    }
}

<# 解析命令行参数并执行对应函数 #>
if ($args.Count -eq 0) {
    Write-Host "请指定要执行的目标: init, showConfig, runDataset, showData"
    exit 1
}

$target = $args[0]
switch ($target) {
    "init" { Invoke-Init }
    "showConfig" { Invoke-ShowConfig }
    "runDataset" { Invoke-RunDataset }
    "showData" { Invoke-ShowData }
    default { Write-Host "未知目标: $target"; exit 1 }
}