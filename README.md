# Cocoanut-bot

Discord bot for OCRing Korean manhwa images with EasyOCR and translating the result with Gemini.

## checkpoint 1
* The bot is runnable

## checkpoint 2
* The ocr is working mock only with the the one chosen being "easy ocr" but the uploaded picture must be clear, no blur text.

## checkpoint 3
* The ocr work well now the bot and read korean text on the image but no blur.

# How to setup after installing everything

### 1. First open vs code
- Open vs code
- Go to the top left and click file
- Click open folder
- Now open the folder that you download name Cocoanut-bot
### 2. Start docker
- Go to window/mac search
- Search for docker desktop
- Open docker desktop
- Wait for docker engine to start
### 3. DockerCompose
- Go back to vs code
- Click terminal on top bar
- Click new terminal
- Then you should see something similar to this on the bottom of the screen
<img width="848" height="231" alt="image" src="https://github.com/user-attachments/assets/27eba9c9-b6a1-43ff-8186-c8a498532740" />
- When you are there type

```
docker compose up -d
```

#### Command above is for starting the bot

```
docker compose down
```

## Daily translation allowance

Each Discord user can submit 80 supported images per day across all servers
and channels. `$check_limit` shows the remaining allowance. It resets at
00:00 Thailand time (GMT+7), regardless of the host timezone or downtime.
Up to 5 attachments are allowed per command. Unsupported files do not count;
accepted image attempts count even if processing later fails. Batches above
the remaining allowance are rejected without consuming any allowance.

Counts are stored in the plain JSON file `data/usage.json`, with no database
dependency. The `bot_data` Docker volume preserves it across restarts and
rebuilds. Keep that volume (avoid `docker compose down -v`). Local Mac runs
use their own `data/` folder. Run one bot process per usage file. Writes use
a temporary file and atomic replacement to avoid partially saved JSON.

Transfer the changes to Linux and run `docker compose up -d --build` to apply.
