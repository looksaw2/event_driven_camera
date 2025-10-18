init:
	@echo "开始安装uv(失败请手动安装)"
	@curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "安装uv成功"
	@echo "启动虚拟环境"
	@uv init
	@uv venv
	@echo "启动虚拟环境成功"
	@echo "同步依赖"
	@uv sync
	@echo "同步虚拟环境成功"
showConfig:
	@echo "start to run the config.py file"
	@python -m src.config.config
	@echo "Finish ..........................."
runDataset:
	@echo "start to show the loaddataset.py file"
	@python -m src.dataset.loadDataset
	@echo "Finish.........................."

showData:
	@echo "开始展示数据可视化"
	@uv run ./src/visualization/plot.py
	@echo "结束，已保存./tmp/img当中请用浏览器打开"

.PHONY: init showConfig runDataset showData