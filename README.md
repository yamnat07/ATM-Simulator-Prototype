# ATM Simulator (Prototype)

A desktop ATM simulator written in Python with tkinter. The window looks like a small ATM: the bank logo and the entry screens are on the left, and four option buttons are in a column on the right. Customer data is kept in a JSON file, and every transaction is recorded in a CSV file.

> **Status: prototype.** It works from start to finish, but it is the first version. A finished version, with the improvements listed under [Known limitations](#known-limitations), is being built separately.

**The bank in this project is fictional.** "Supreme Bank of India" is a made-up name, and the logo is an original drawing. All customers, account numbers, card numbers, PINs and balances are invented sample data.

## Contents

- [Features](#features)
- [Requirements](#requirements)
- [How to run](#how-to-run)
- [Try it with the sample data](#try-it-with-the-sample-data)
- [How each option works](#how-each-option-works)
- [How your data is stored](#how-your-data-is-stored)
- [The transaction log](#the-transaction-log)
- [Testing](#testing)
- [Known limitations](#known-limitations)
- [Files in this repository](#files-in-this-repository)
- [How it was built](#how-it-was-built)
- [Planned for the finished version](#planned-for-the-finished-version)

## Features

- Four options: **Withdraw**, **Deposit**, **Check Balance** and **Change PIN**
- Every option asks for the account number and PIN first
- Balances are kept in rupees and paise (two decimal places) and shown like `₹30,430.75`
- Input checks with clear messages: empty fields, unknown account, wrong PIN, invalid amounts, and not enough balance
- A new PIN must be exactly 4 digits, typed twice, and different from the old one
- PIN boxes show `*` instead of the digits
- Changes are saved straight away to `customers.json`, using a safe write (temporary file first, then a swap), so the file is never left half-written
- Every successful operation adds a row to `log.csv`
- The program finds its own files wherever it is started from

## Requirements

- **Python 3.12 or newer.** The code uses f-strings that repeat the same quote character inside the braces, which older versions do not accept.
- **tkinter.** It comes with the standard Python installer on Windows and macOS. On some Linux systems you need to install it separately (for example `sudo apt install python3-tk`).
- **Pillow**, used to load and resize the logo:

```
pip install pillow
```

## How to run

1. Put these three files in the same folder: `atm-simulator.py`, `customers.json` and `bank_logo_supreme.png`.
2. Open a terminal in that folder and run:

```
python atm-simulator.py
```

(On some systems the command is `python3`.)

The program changes into its own folder when it starts, so it also works if you start it from somewhere else or from an editor. `log.csv` is created automatically the first time a transaction is recorded.

If `customers.json` or the logo is missing, the program stops with a Python error message. See [Known limitations](#known-limitations).

## Try it with the sample data

The sample customers are in `customers.json`. For example:

| Account No. | Name |
|-------------|------|
| 1001234501 | Aarav Sharma |
| 1001234502 | Priya Verma |
| 1001234507 | Karan Malhotra |

Open the file to see each customer's PIN and balance. Remember that Withdraw, Deposit and Change PIN modify this file, so keep a copy of the original if you want to start from the same data again.

Things worth trying:

- Leave fields empty, or enter a wrong PIN or an unknown account number
- Withdraw more than the balance
- Enter amounts such as `abc`, `0`, `-5` or `12.345`
- Change a PIN to `123`, to `12345`, or to the same PIN as before
- Do several operations in a row (the main screen comes back after each successful one)

## How each option works

| Option | What you enter | What happens |
|--------|----------------|--------------|
| **Withdraw** | Account No., PIN, amount | Takes the amount off the balance. Refused if the amount is invalid or bigger than the balance. |
| **Deposit** | Account No., PIN, amount | Adds the amount to the balance. There is no upper limit. |
| **Check Balance** | Account No., PIN | Shows the available balance. Nothing is changed. |
| **Change PIN** | Account No., old PIN, new PIN, new PIN again | Saves the new PIN if every check passes. |

Rules for amounts: whole rupees, or rupees with 1 or 2 paise digits (`500`, `500.5`, `500.50`). Zero, negative numbers, letters, more than two decimals and forms such as `1e3` or `nan` are refused.

After a successful operation a message is shown and the program returns to the main screen.

## How your data is stored

Customers are in `customers.json`, stored under their account number:

```json
{
    "1001234501": {
        "name": "Aarav Sharma",
        "card_number": "4000125678901201",
        "pin": "4828",
        "balance": 30430.75
    }
}
```

- The account number, card number and PIN are text, so a PIN such as `0376` keeps its leading zero.
- The balance is a number and is rounded to two decimals after every change.
- The PIN is stored as plain text in this version. See [Known limitations](#known-limitations).

## The transaction log

Each successful operation adds one row to `log.csv`: date, time, account number and what happened.

```
30-October-2026,01:12:33 PM,Account No.:1001234504,Money Deposited:10000.0
30-October-2026,01:15:06 PM,Account No.:1001234502,Money Deposited:1500.98
```

The log never contains PINs. A PIN change is recorded as just `PIN Changed`.

## Testing

The program logic was tested by running the real code with scripted input, on copies of the data. The tkinter window and the message boxes were replaced by stand-ins for these tests, so the checks covered what the program decides and saves, not how the screens look. **65 checks passed**, including:

- every warning message for empty fields, unknown accounts and wrong PINs
- invalid amounts (`abc`, `-5`, `0`, `0.00`, `12.345`, `1e3`, `nan`, `5 5`)
- withdrawing more than the balance, and withdrawing the whole balance
- depositing more than the current balance (allowed)
- correct balances after small amounts such as `0.1` and `0.2`
- every refusal rule for a new PIN, and a new PIN that starts with `0`
- the old PIN failing and the new PIN working after a change
- six operations in a row, returning to the main screen each time
- log rows added after existing ones, with no blank lines and no PINs
- no leftover temporary file after saving
- other customers' data staying untouched

The screens (layout, colours, images) were checked by hand by the author, not by the scripted tests.

## Known limitations

- **No Cancel button yet.** Once an option is opened, the only way back to the main screen is to finish the operation.
- **PINs are stored as plain text.** A real system would store only a hash.
- **No lockout.** A wrong PIN can be tried any number of times.
- **The 5-second wait is `time.sleep`,** which freezes the window while it runs.
- **`log.csv` has no header row,** and labels such as `Account No.:` are part of the values, which makes it awkward to analyse.
- **If `customers.json` is missing or damaged,** the program stops with a raw Python error instead of a friendly message.
- **No account opening or closing,** and no card-number login. The account number is used to identify the customer.
- **A single shared data file.** Two copies of the program running at once would overwrite each other's changes.
- Tested with Python 3.13 on the logic level; the screens were tried by hand on the author's computer only.

## Files in this repository

| File | Purpose |
|------|---------|
| `atm-simulator.py` | The program |
| `customers.json` | Sample customer data (all invented) |
| `bank_logo_supreme.png` | The bank logo shown on the screen |
| `README.md` | This file |

`log.csv` and `customers.tmp` are created while the program runs, so they are not part of the repository.

## How it was built

The program is one script with a function for each option (`withdraw`, `deposit`, `check_balance`, `change_pin`), a `main()` function that draws the main screen and the menu buttons, and small helpers for saving the data, writing the log and reading the date and time.

The main things practised:

- Building a tkinter window with a `Canvas`, `Entry` boxes and `Button`s
- Placing widgets by coordinates and swapping the screen contents
- Reading and writing JSON, and appending to a CSV file
- Input validation with regular expressions (`re.fullmatch`)
- Formatting dates and times with `datetime`
- Safe saving with a temporary file and `os.replace`

I wrote the program step by step. Claude, an AI assistant, reviewed my code, tested the logic, and suggested fixes along the way. A few pieces, such as the starter data and the safe-saving function, came from those suggestions. The design and the decisions about how the program behaves were mine.

## Planned for the finished version

- A Cancel button on every screen
- Hashed PINs and an account lock after 3 wrong attempts
- A clean `log.csv` with a header and one value per column, so it can be analysed with pandas
- A mini statement showing the last transactions
- A non-freezing "please wait" animation (a GIF, with `window.after` instead of `time.sleep`)
- Logic separated from the screens, so it can be tested without a window
- Friendly messages for missing or damaged files
