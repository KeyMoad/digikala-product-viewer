
# Digikala Product Viewer

A bot designed to generate views for your products on Digikala.

## Features

- **Automated Viewing**: Simulates user interactions to increase product views.
- **Configurable Settings**: Easily adjust parameters via the `config.yaml` file.
- **Product Management**: Manage target products through the `id_list.txt` file.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/KeyMoad/digikala-product-viewer.git
   cd digikala-product-viewer
   ```

2. **Run the installer Bash script**:
   ```bash
   bash scripts/install.sh
   ```

## Configuration

1. **Product IDs**:
   - Add the IDs of the products you want to target in the `id_list.txt` file, each on a new line.

2. **Settings**:
   - Adjust the `config.yaml` file to configure the bot's behavior, such as the number of views to generate, time intervals between actions, etc.

## Usage

Run the bot using the following command:

```bash
python main.py
```

The bot will read the product IDs from `id_list.txt` and use the settings specified in `config.yaml` to simulate views on Digikala.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Disclaimer**: This tool is intended for educational and research purposes only. Use it responsibly and ensure compliance with Digikala's terms of service.
