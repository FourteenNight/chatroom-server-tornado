/*
 Navicat Premium Data Transfer

 Source Server         : 聊天室
 Source Server Type    : MongoDB
 Source Server Version : 40415
 Source Host           : localhost:20027
 Source Schema         : chatroom

 Target Server Type    : MongoDB
 Target Server Version : 40415
 File Encoding         : 65001

 Date: 16/10/2022 19:37:54
*/


// ----------------------------
// Collection structure for group_chat_message
// ----------------------------
db.getCollection("group_chat_message").drop();
db.createCollection("group_chat_message");

// ----------------------------
// Documents of group_chat_message
// ----------------------------

// ----------------------------
// Collection structure for private_chat_message
// ----------------------------
db.getCollection("private_chat_message").drop();
db.createCollection("private_chat_message");

// ----------------------------
// Documents of private_chat_message
// ----------------------------

// ----------------------------
// Collection structure for user_group_chat
// ----------------------------
db.getCollection("user_group_chat").drop();
db.createCollection("user_group_chat");

// ----------------------------
// Documents of user_group_chat
// ----------------------------

// ----------------------------
// Collection structure for users
// ----------------------------
db.getCollection("users").drop();
db.createCollection("users");

// ----------------------------
// Documents of users
// ----------------------------
db.getCollection("users").insert([ {
    _id: ObjectId("62d015d4f4050000ab003663"),
    name: "王根基",
    "creation_time": "2022-7-14 22:17",
    account: "root",
    pwd: "wanggenji",
    type: "manage",
    online: false,
    wsid: "",
    cookie: ""
} ]);
db.getCollection("users").insert([ {
    _id: ObjectId("62d022d470ea98c9308bd355"),
    name: "张三",
    type: "user",
    "creation_time": "2022-7-14 22:17",
    account: "admin",
    pwd: "admin",
    online: false,
    wsid: "",
    cookie: ""
} ]);
