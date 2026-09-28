# Yuanshan Xu (徐元山)

Master's student at Harbin Institute of Technology. My research is multimodal sensor simulation: generating visible, infrared and SAR imagery of the same scene in Unreal Engine 5. Outside research, I build tools and plugins for AI coding agents such as Claude Code and DeepSeek Harness.

## Research

- **Visible / infrared / SAR simulation in Unreal Engine 5.** A single capture produces a visible image, an 8–14 μm infrared radiance image and a SAR image of the same scene.
- **raysar-rust** *(private)*. A Rust port of the RaySAR SAR simulator, covering both the POV-Ray-based ray tracer and the MATLAB image formation. It removes both dependencies, reproduces the original tracer's output on calibration scenes, matches the official MATLAB imaging to within 6×10⁻¹⁶ of peak, and cuts end-to-end SAR generation from 79.9 s to 10.2 s.

## Selected projects

- **[Ai-Report-Formatter](https://github.com/BeiZi6/Ai-Report-Formatter)**: offline-first desktop app that turns Markdown into submission-ready Word documents, with live preview, configurable academic styles, numbered equations, IEEE / GB/T / APA references from BibTeX, and batch export. Released for macOS, Windows and Linux.<br>*Electron · Next.js · Python · Rust*
- **[CSwitch](https://github.com/BeiZi6/CSwitch)**: desktop app that runs a local Anthropic-compatible gateway so Claude Science can use third-party models, maps its model picker to upstream model IDs, and launches it with an isolated data directory.<br>*Electron · TypeScript*
- **[dsh-theme-plugin](https://github.com/BeiZi6/dsh-theme-plugin)**: theme studio for the DeepSeek Harness web GUI with five presets, per-mode colors and fonts, and 70+ derived design tokens, applied live through the official plugin APIs.<br>*JavaScript*
- **[dsh-opencodego-usage](https://github.com/BeiZi6/dsh-opencodego-usage)**: OpenCodeGo quota monitor for the DeepSeek Harness web GUI, with a color-coded indicator and a rolling / weekly / monthly usage panel.<br>*JavaScript*
- **[claude-3p-setup](https://github.com/BeiZi6/claude-3p-setup)**: one-command setup for third-party API gateways in Claude Desktop on macOS and Windows, with model discovery, named profiles and automatic backups.<br>*Bash · PowerShell*
- **[easy-cc](https://github.com/BeiZi6/easy-cc)**: a Chinese guide to Claude Code, from first run to hooks, subagents, MCP and CI automation.<br>*Markdown · Obsidian*

## Tech stack

- **Languages:** Python, Rust, TypeScript / JavaScript, MATLAB, Go
- **Tools:** Unreal Engine 5, Electron, Next.js / React, Tauri, Git

## Education

- **Harbin Institute of Technology**, Master's student, 2026 – present
- **Harbin Institute of Technology, Weihai**, B.Eng. in Electronic Information Engineering
