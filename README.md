# Discord Ticket Bot

A modular and feature-rich Discord Ticket Bot built with `discord.py 2.x`. This bot allows users to create support tickets via a dropdown menu and provides ticket management features like closing, deleting, and generating transcripts.

## Features

- **🎫 Ticket Creation with Dropdown Panel**
  - Use the `!tc` command (admin-only) to send an embed with a dropdown menu for ticket types: General, Report, or Suggestion.
  - Each ticket type creates a dedicated channel with custom permissions for the user and support team.

- **✅ Automatic Ticket Numbering**
  - Ticket numbers are stored in `ticket_counter.json` and formatted as 4-digit IDs (e.g., `0001`, `0002`).
  - Channel names reflect ticket type:
    - General: `🛠️-0001`
    - Report: `🚨-0002`
    - Suggestion: `💡-0003`

- **📝 Professional Embed Templates**
  - Each ticket type has a unique embed with a title, description, and distinct color.
  - Embeds include a footer showing the ticket creator's username.

- **🔒 Ticket Control Buttons**
  - **Close**: Removes the ticket creator’s access to the channel but keeps it for support staff.
  - **Delete**: Deletes the ticket channel and removes it from the open tickets list.
  - **Transcript**: Generates an HTML transcript of the ticket conversation.

- **💾 Transcript System**
  - Generates an in-memory `.html` transcript using `BytesIO`

- **📊 Bot Status Updates**
  - Updates bot activity every 15 seconds, alternating between:
    - `🎫 Open: X` (number of open tickets).
    - `🔒 Closed: Y` (number of closed tickets).

- **🔹 Role-Based Permissions**
  - Only the ticket creator or users with the support role (`SUPPORT_ROLE_ID`) can close or delete tickets.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/SinaSeifi-f/Discord_Ticket.git
   cd Discord_Ticket
   ```

2. **Install Dependencies**
   Ensure you have Python 3.8+ installed, then run:
   ```bash
   pip install -r requirements.txt
   ```
   Required packages:
   - `discord.py>=2.0.0`
   - `python-dotenv`

3. **Configure Environment**
   - Edit a `.env` file in the `utils` directory.
   - Add the following:
     ```env
     BOT_TOKEN=your_discord_bot_token
     TICKET_CATEGORY_ID=your_category_id
     SUPPORT_ROLE_ID=your_support_role_id
     ```

4. **Run the Bot**
   ```bash
   python bot.py
   ```

## Usage

1. **Start the Bot**
   - Run `python bot.py` to start the bot.
   - The bot will load cogs from the `cogs/` folder and initialize the ticket counter.

2. **Create a Ticket Panel**
   - Use the `!tc` command (admin-only) to send a ticket creation panel with a dropdown menu.
   - Example:
     ```
     !tc
     ```
     This sends an embed with a dropdown for General, Report, or Suggestion tickets.

3. **Open a Ticket**
   - Select an option from the dropdown to create a ticket channel.
   - The bot creates a channel (e.g., `🛠️-0001`) with permissions for the user and support team.

4. **Manage Tickets**
   - Inside the ticket channel, use the buttons:
     - **Close**: Restricts user access.
     - **Delete**: Deletes the channel.
     - **Transcript**: Downloads an HTML transcript of the conversation.

## Project Structure

```
discord-ticket-bot/
├── cogs/
│   ├── panel.py          # Handles ticket panel command and dropdown
│   ├── ticket.py         # Manages ticket creation, buttons, and status
├── utils/
│   ├── config.py         # Bot configuration (token, category, role IDs)
│   ├── counter.py        # Manages ticket counter and JSON storage
│   ├── transcript.py     # Generates HTML transcripts
├── main.py               # Main bot script
├── ticket_counter.json   # Stores ticket counter data
├── .env                  # Environment variables (not tracked)
├── README.md             # This file
```

## Example Commands

- **Create Ticket Panel**:
  ```
  !tc
  ```
  Sends a ticket panel with a dropdown menu.

- **Interact with Tickets**:
  - Select a ticket type from the dropdown to create a channel.
  - Use the buttons in the ticket channel to close, delete, or generate a transcript.

## Notes

- Ensure the bot has the necessary permissions (`Manage Channels`, `Send Messages`, `Embed Links`, etc.).
- The bot uses `discord.py 2.x` and supports slash commands/interactions.
- Error handling is implemented to ensure smooth operation.
- Transcripts are generated in-memory and not saved to disk.

## Contributing

Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
