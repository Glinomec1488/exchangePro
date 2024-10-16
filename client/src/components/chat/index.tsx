import { useState, useEffect } from "react";
import Chat, { Message } from "react-simple-chat";
import "react-simple-chat/src/components/index.css";
import "./styles.css";
import chatIcon from "../../assets/openChat.png";
import sendIcon from "../../assets/sendMessage.png";
import useChat from "./useChat";

const CustomChat = () => {
  const { messages, sendMessage } = useChat();

  return null;
  /*<Chat
      minimized
      headerStyle={{
        borderBottom: "2px solid #9500da7a",
        boxShadow: "0px 4px 2px -2px #9500da38",
      }}
      containerStyle={{
        position: "fixed",
        boxShadow: "0 0 10px 0 #9500da",
      }}
      leftBubbleStyle={{
        backgroundColor: "#9500da",
      }}
      rightBubbleStyle={{
        backgroundColor: "#9500da",
      }}
      chatIcon={chatIcon}
      sendIcon={sendIcon}
      title="Support"
      user={{ id: 2 }}
      messages={messages}
      onSend={(message) => sendMessage(message)}
    />*/
};

export default CustomChat;
