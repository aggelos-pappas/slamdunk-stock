# SlamDunk Raffle Discord Bot  

This is a Discord bot that retrieves and displays information about raffle products from [SlamDunk](https://raffle.slamdunk.gr). It provides details about available sizes, stock, price, and raffle end date, presented neatly in an embedded message.

---

## 🚀 Features  
- Fetches raffle product details from SlamDunk's API.
- Displays product image, price, available sizes, and stock.
- Shows the end date of the raffle, converted to Discord's time format.
- Neatly organized in a Discord embed message.

---

## 🛠️ Requirements  
- Python 3.8+
- Required Packages:
  - `discord.py`: For interacting with the Discord API.
  - `curl_cffi`: For making HTTP requests (faster and safer alternative to `requests`).
  - `pytz`: For handling timezone conversions.
  - `tzdata`: Required on some systems for timezone support (optional).

---

## 📦 Installation  

1. **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/slamdunk-raffle-bot.git
    cd slamdunk-raffle-bot
    ```

---

## ⚙️ Usage  

### 1. **Run the Bot:**
```bash
python slam.py
```
