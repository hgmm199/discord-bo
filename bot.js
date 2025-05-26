const { Client, GatewayIntentBits, PermissionsBitField } = require('discord.js');

const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent
  ]
});

const TOKEN = 'MTM3NjQ3NDU3MzUxOTcxNjQyMg.GM1i2t.ydCIztqI3UcGxfZsEDnfDU-5h4paRwJdJvHpvA';
const OWNER_ID = '1360479539515490365';

client.once('ready', () => {
  console.log(`✅ Bot đã sẵn sàng: ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
  if (message.author.bot) return;
  if (!message.content.startsWith('oclear')) return;

  if (message.author.id !== OWNER_ID) {
    return message.reply('❌ Chỉ chủ sở hữu bot mới được sử dụng lệnh này.');
  }

  const args = message.content.split(' ');
  const amount = parseInt(args[1]);

  if (isNaN(amount) || amount < 1 || amount > 100) {
    return message.reply('⚠️ Hãy nhập số lượng từ 1 đến 100. Ví dụ: `?xóa 10`');
  }

  try {
    await message.channel.bulkDelete(amount + 1, true);
    const msg = await message.channel.send(`🧹 Đã xóa ${amount} tin nhắn.`);
    setTimeout(() => msg.delete(), 3000);
  } catch (err) {
    console.error(err);
    message.reply('❗ Có lỗi xảy ra khi xóa tin nhắn.');
  }
});

client.login(TOKEN);
