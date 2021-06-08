const auditTypeDict = new Map();

auditTypeDict.set(1, 'Updated the Server');
auditTypeDict.set(10, 'Created a New Channel');
auditTypeDict.set(11, 'Updated a Channel');
auditTypeDict.set(12, 'Deleted a Channel');
auditTypeDict.set(13, 'Created Channel Overwrites');
auditTypeDict.set(14, 'Updated Channel Overwrites');
auditTypeDict.set(15, 'Deleting Channel Overwrites');
auditTypeDict.set(20, 'Kicked a Memeber');
auditTypeDict.set(21, 'Pruned a Member');
auditTypeDict.set(22, 'Banned a Member');
auditTypeDict.set(23, 'Unbanned a Member');
auditTypeDict.set(24, 'Updated a Member');
auditTypeDict.set(25, 'Updated a Member\'s Role');
auditTypeDict.set(26, 'Moved a Member');
auditTypeDict.set(27, 'Disconnected a Member');
auditTypeDict.set(28, 'Added a Bot');
auditTypeDict.set(30, 'Created a Role');
auditTypeDict.set(31, 'Updated a Role');
auditTypeDict.set(32, 'Deleted a Role');
auditTypeDict.set(40, 'Created an Invite');
auditTypeDict.set(41, 'Updated an Invite');
auditTypeDict.set(42, 'Deleted an Invite');
auditTypeDict.set(50, 'Created a Webhook');
auditTypeDict.set(51, 'Updated a Webhook');
auditTypeDict.set(52, 'Deleted a Webhook');
auditTypeDict.set(60, 'Created a Emoji');
auditTypeDict.set(61, 'Updated a Emoji');
auditTypeDict.set(62, 'Deleted a Emoji');
auditTypeDict.set(72, 'Deleted a Message');
auditTypeDict.set(73, 'Purged Messages');
auditTypeDict.set(74, 'Pinned a Message');
auditTypeDict.set(75, 'Unpinned a Message');
auditTypeDict.set(80, 'Created an Integration');
auditTypeDict.set(81, 'Updated an Integration');
auditTypeDict.set(82, 'Deleted an Integration');

export default auditTypeDict