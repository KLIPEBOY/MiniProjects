# Random Password Generator Bot

This Telegram bot generates random passwords based on user preferences.

## How to Use

1. Start the bot by sending the `/start` command.
2. Initiate the password generation process by sending the `/generate` command.
3. Follow the prompts to customize your password:
   - Choose whether to include digits.
   - Choose whether to include symbols.
   - Select the length of the password.
4. The bot will generate and send the random password.

## Commands

- `/start`: Start the bot and receive a welcome message.
- `/generate`: Initiate the password generation process.

## Inline Buttons

- "Да" / "Yes": Confirm to include the specified option (digits or symbols).
- "Нет" / "No": Reject the specified option (digits or symbols).
- Number buttons: Select the length of the password.
- "Другое" / "Custom": Enter a custom length for the password.

## Callbacks

- The bot handles inline button callbacks to adjust user preferences for digits, symbols, and password length.

## Dependencies

- Telebot: Python library for Telegram bot development.
- Random: Python built-in library for generating random data.
- String: Python built-in library for string manipulation.

## License

This project is licensed under the [MIT License](LICENSE).

