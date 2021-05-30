const { ShardingManager } = require('discord.js');
const settings = require('./settings.json')
const manager = new ShardingManager('./bot.js', { token: settings.discord_token });

manager.on('shardCreate', shard => console.log(`Launched JARVIS shard ${shard.id}`));
manager.spawn(settings.jarvis_shard_count);