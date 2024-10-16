import { useState, useEffect, useCallback } from "react";
import { Message } from "react-simple-chat";
import { serveUrl } from "../../config";

const useChat = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello my friend!",
      createdAt: "2021-07-21 12:09:12",
      user: {
        id: 1,
      },
    },
    {
      id: 2,
      text: "Hello!",
      createdAt: "2021-07-21 14:09:12",
      user: {
        id: 2,
      },
    },
  ]);

  const getHistoy = async () => {
    const userId = localStorage.getItem("userId");

    const history = await fetch(`${serveUrl}/msgHistory/${userId}`).then(
      (res) => res.json()
    );

    if (history.length > 0) {
      setMessages(
        history.map((elem: any) => ({
          id: elem.id,
          text: elem.text,
          createdAt: elem.timestamp,
          user: {
            id: elem.user === "true" ? 2 : 1,
          },
        }))
      );
    }
  };

  const sendMessage = async (message: Message) => {
    const userId = localStorage.getItem("userId");
    const timestamp = new Date().getTime();
    await fetch(
      `${serveUrl}/msgSave/${message.text}/${userId}/${timestamp}/true`,
      {
        method: "POST",
      }
    );

    getHistoy();
  };

  useEffect(() => {
    const timer = setInterval(() => {
      getHistoy();
    }, 5000);

    return () => clearInterval(timer);
  });

  return {
    messages,
    sendMessage,
  };
};

export default useChat;
