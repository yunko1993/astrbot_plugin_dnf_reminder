# 🔔 DNF 私人提醒秘书 (AstrBot Plugin)

专门为 DNF 玩家打造的通用定时提醒插件，再也不怕忘领心悦增幅器、助手编年史！

## 🚀 快速安装

在 AstrBot 控制台中输入以下指令即可一键安装：

```text
/plugin install https://github.com/yunko1993/dnf_personal_reminder
```

或者手动将本仓库代码放入 `plugins/dnf_personal_reminder` 目录下。

## ✨ 功能亮点

- **🔒 绝对隐私**：无论你在群里还是私聊中添加，提醒消息一律通过 **【私聊】** 发送，不打扰他人。
- **📝 自助管理**：用户可自行增删改属于自己的提醒任务。
- **💾 数据隔离**：插件代码与数据分离，更新插件不影响已保存的提醒设置。

## 🎮 指令说明

所有指令前缀均为 `/提醒`。

| 功能 | 指令示例 |
| :--- | :--- |
| **添加提醒** | `/提醒 添加 10:00 领心悦增幅器` |
| **查看列表** | `/提醒 列表` |
| **删除提醒** | `/提醒 删除 0` |
| **立即测试** | `/提醒 立即测试` |

> **提示**：建议将领奖直达链接写在内容里，手机点击直接领奖。
> 示例：`/提醒 添加 10:30 领心悦 https://act.xinyue.qq.com/act/a20231103dnf/index.html`

## 📂 数据存放
用户设置的提醒数据保存在：`data/plugin_data/dnf_personal_reminder/reminders.json`

## 📜 许可证
[MIT License](LICENSE)
