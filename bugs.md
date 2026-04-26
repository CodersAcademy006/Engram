# Ghost-OS: Roadmap to Production

This document tracks all known bugs, required features, and improvements to make Ghost-OS a production-ready application.

---

## 🐛 Bugs & Weak Spots

These are issues that need to be fixed for the application to be stable and secure.

-   **[BUG-001] No Encryption at Rest:**
    -   **Problem:** All captured data (screenshots, audio chunks) and the vector database are stored unencrypted on the disk. This is a major security risk for a "privacy-first" application.
    -   **Solution:** Implement file-level encryption for all data in the `data/` directory. The application should handle decryption in memory when processing or retrieving data.

-   **[BUG-002] Lack of Error Handling & Resilience:**
    -   **Problem:** The system uses a file-based queue. If a processing script fails on a file, it might get stuck in a loop or crash the process, leading to data loss. There is no robust error handling.
    -   **Solution:** Implement try-except blocks for all major operations (file I/O, model inference). Create a mechanism to move "poison pill" files (files that consistently cause errors) to a separate quarantine directory.

-   **[BUG-003] Hardcoded Paths and Configuration:**
    -   **Problem:** Many paths and settings (e.g., model names, data directories) are hardcoded in the source code. This makes the application brittle and hard to configure.
    -   **Solution:** Move all configuration into a central `config.py` or a `config.yaml` file. The application should load all settings from this single source of truth.

-   **[BUG-004] Manual Ollama Dependency:**
    -   **Problem:** The user must manually install and run the Ollama service before starting the application. The application does not handle the case where Ollama is not running.
    -   **Solution:** The UI should detect if the Ollama service is unreachable and show a clear error message with instructions. This will later be improved by the model fallback system (see FEAT-005).

---

## ✨ New Features & Improvements

These are features needed to transform Ghost-OS from a developer tool into a user-friendly application.

-   **[FEAT-001] Application Packaging:**
    -   **Goal:** Create a single executable file (`.exe` for Windows, `.app` for macOS) so users don't need to install Python or run `pip install`.
    -   **Tool:** Use `PyInstaller` or `cx_Freeze` to package the entire application.

-   **[FEAT-002] Major UI/UX Overhaul:**
    -   **Goal:** Move from a single-page chat app to a multi-page dashboard.
    -   **Plan:**
        -   Implement a sidebar for navigation.
        -   Create a "Memory Wall" page to browse, search, and delete memories.
        -   Create a "Settings" page for configuration.
        -   Add a master On/Off switch for the recording services.

-   **[FEAT-003] Memory Management:**
    -   **Goal:** Give users full control over their data.
    -   **Plan:** In the "Memory Wall" UI, add functionality to delete individual memories or bulk-delete data based on date ranges.

-   **[FEAT-004] Centralized Logging:**
    -   **Goal:** Make it easier to debug issues.
    -   **Plan:** Configure the Python `logging` module to write logs from all processes to a single, rotating log file.

-   **[FEAT-005] LLM Fallback System:**
    -   **Goal:** Make the application work even if the user doesn't have a local Ollama model.
    -   **Plan:** Modify the `GhostBrain` class to support multiple models. It should try the local Ollama first, and if it fails, it should cycle through a list of fallback models using the user's provided API keys.

-   **[FEAT-006] Onboarding & First-Run Experience:**
    -   **Goal:** Guide the user when they first open the application.
    -   **Plan:** On first launch, show a welcome screen that explains what the app does, asks for necessary permissions (if any), and helps them configure basic settings.

---
## 🗣️ Our Conversation & Changes

- **Our Goal:** Make this project production-ready.
- **My Role:** Senior Engineer, I find problems and write code.
- **Your Role:** Big Chief / Sole Author. You make all commits and manage the GitHub repository.
- **Our Plan:** We created this `bugs.md` file as our roadmap. We will pick items from this list, I will code the solution, and you will commit it.
- **Changes Made By Me:**
    - I have analyzed the entire repository.
    - I have created this `bugs.md` file to document our plan and all required work.
