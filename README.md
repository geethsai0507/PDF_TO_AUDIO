# English PDF To Audio Conversion 🎧📄

A lightweight, open-source Streamlit app that transforms any English PDF into spoken audio using **edge-tts** and **deep-translator**. Upload your PDF, pick from dozens of multilingual voices, and get a high-quality MP3—all without collecting any user data.

---

## 🚀 Features

- **PDF → Audio in One Click**  
  Upload your PDF, translate it into the selected language, and convert to MP3.

- **Multilingual Voices**  
  Powered by Microsoft’s Edge TTS: 70+ neural voices across 40+ locales.

- **Automatic Chunking & Translation**  
  Splits large documents into safe, translatable chunks to avoid API limits.

- **Fun “Hang Tight” UX**  
  Stoic quotes and animations keep you entertained during synthesis.

- **100% Open Source**  
  No telemetry, no paywalls—self-host or modify as you like.

---

## 📦 Requirements

- Python 3.8 or newer  
- [Streamlit](https://streamlit.io/)  
- [PyPDF2](https://pypi.org/project/PyPDF2/)  
- [deep-translator](https://pypi.org/project/deep-translator/)  
- [edge-tts](https://pypi.org/project/edge-tts/)  
- [pycountry](https://pypi.org/project/pycountry/)  
- `ffmpeg` installed and in your PATH (required by edge-tts)

---

## ⚙️ Installation & Usage

1. **Clone the repo**  
   ```bash
   git clone https://github.com/yourusername/english-pdf-to-audio.git
   cd english-pdf-to-audio


2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

5. **In your browser**

   * Browse supported voices, choose one
   * Upload an English PDF
   * Click **Translate PDF Text** → **Convert to Audio**
   * Play or download your MP3!

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to your branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📫 Contact

For questions, feedback or collaboration, reach me at:
**[geethsai0507@gmail.com](mailto:geethsai0507@gmail.com)**

> *Thank you for using English PDF To Audio Conversion!*

```
```
