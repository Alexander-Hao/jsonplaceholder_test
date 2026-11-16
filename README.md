# API 接口自动化测试框架（pytest + requests）

基于 **pytest + requests** 的分层接口自动化测试项目，采用"接口对象"设计思想，
覆盖 **用户模块 / 帖子模块** 的增删改查全流程，支持 **数据驱动（YAML）**、
**统一日志**、**失败重试** 与 **HTML 测试报告**。

> 被测服务使用公开 Mock API（JSONPlaceholder，免费稳定、无需鉴权），
> 用于模拟真实业务系统的用户 / 内容管理接口，可无缝切换到公司真实环境。

## 技术栈

| 组件 | 说明 |
|---|---|
| Python 3.10+ | 开发语言 |
| pytest | 测试框架：fixture、参数化、标记（mark）、钩子函数 |
| requests | HTTP 请求库（统一封装于 RequestClient） |
| pytest-html | 自动化测试报告（HTML） |
| PyYAML | 测试数据文件解析（数据驱动） |
| logging | 标准日志：控制台 + 滚动文件双输出 |

## 目录结构

```
API test/
├── pytest.ini              # pytest 配置（用例收集、报告输出、mark 注册）
├── requirements.txt        # 依赖清单
├── run.py                  # 一键运行入口
├── config/
│   └── settings.py         # 全局配置：BASE_URL / 超时 / 重试策略 / 输出路径
├── common/
│   ├── request_client.py   # requests 统一封装：日志、超时、失败自动重试
│   ├── assert_util.py      # 断言封装：状态码 / JSON 字段 / 列表长度 / 批量匹配
│   └── logger.py           # 日志封装（RotatingFileHandler 滚动文件）
├── api/
│   ├── base_api.py         # 接口基类（接口对象模式，类似 PO）
│   ├── user_api.py         # 用户模块接口：列表/详情/新增/更新/删除
│   └── post_api.py         # 帖子模块接口：列表/详情/新增/更新/删除
├── testcases/
│   ├── conftest.py         # 共享 fixture：会话日志、用例日志、报告标题
│   ├── test_user_api.py    # 用户模块用例（含参数化数据驱动）
│   └── test_post_api.py    # 帖子模块用例（含 YAML 数据驱动）
├── data/
│   └── posts.yaml          # 参数化测试数据（数据与代码分离）
├── docs/
│   └── api_document.md     # 接口测试文档（接口说明 + 用例覆盖映射）
├── reports/                # HTML 测试报告输出目录
└── logs/                   # 运行日志输出目录
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行全部用例（自动生成 HTML 报告）
python run.py
# 或
pytest

# 3. 只跑冒烟用例
pytest -m smoke

# 4. 查看报告
# 打开 reports/report.html（浏览器直接打开）
# 运行日志在 logs/api_test.log
```

## 用例覆盖

| 模块 | 用例 | 校验点 |
|---|---|---|
| 用户 | 查询用户列表 | 状态码 200、列表长度 10 |
| 用户 | 查询用户详情 | 状态码 200、id / name 字段 |
| 用户 | 查询不存在的用户 | 状态码 404 |
| 用户 | 数据驱动批量校验 | 参数化 2 组用户姓名 |
| 用户 | 新增 / 更新 / 删除 | 201 / 200 / 200 |
| 帖子 | 按 userId 过滤 | 结果全部属于该用户 |
| 帖子 | 查询详情 | 200、标题非空 |
| 帖子 | YAML 数据驱动详情查询 | 3 组用例（含 404 场景） |
| 帖子 | 发布 / 更新 / 删除 | 201 / 200 / 200 |

## 框架设计要点

1. **分层架构**：`common`（工具）→ `api`（接口对象）→ `testcases`（用例），
   接口变动只改 api 层，用例层专注于业务断言；
2. **接口对象模式**：每个业务模块一个类，URL 拼接与请求细节全部收敛，
   新增接口 = 新增一个方法，新增用例 = 新增一个 test 函数；
3. **数据驱动**：参数化用例的数据从 YAML 文件读取，数据与代码分离，
   新增测试数据不需要改代码；
4. **统一请求封装**：所有请求自动记录日志、统一超时、网络异常自动重试，
   保证了日志可追溯性和用例稳定性；
5. **断言封装**：失败信息包含期望值、实际值、响应体片段，定位问题快；
6. **工程化**：pytest.ini 集中管理配置、smoke 标记区分冒烟与回归、
   pytest-html 报告 + logging 日志双产物。

## 接入其他项目怎么改

1. 把 `config/settings.py` 的 `BASE_URL` 改成被测环境地址；
2. 如需鉴权，在 `RequestClient` 中统一添加 token（从登录接口获取或配置注入）；
3. 在 `api/` 下按业务模块新增接口类，在 `testcases/` 下新增用例文件；