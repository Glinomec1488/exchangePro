import { useState, useEffect, useCallback } from "react";
import { useAppSelector } from "../../store/hooks";
import { Message } from "react-simple-chat";
import { serveUrl } from "../../config";
import { io } from "socket.io-client";
import { chechUserChatBan, chechUserId } from "../../helpers";

const useChat = () => {
  const [isChatBanned, setIsChatBanned] = useState<boolean | null>(null);
  useEffect(() => {
    const fetchChatStatus = async () => {
      const result = await chechUserChatBan(); // Call the async function
      if (result == 1) {
        setIsChatBanned(true);
      } else {
        setIsChatBanned(false);
      }
    };

    fetchChatStatus();
  }, []); // Empty dependency array ensures this runs only on mount
  const [messages, setMessages] = useState<Message[]>([
    /*{
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
    },*/
  ]);

  const getHistoy = async () => {
    const history = await fetch(
      `${serveUrl}/msgHistory/${localStorage.getItem("userId")}`
    ).then((res) => res.json());

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
    const messageTextEncoded = encodeURIComponent(message.text);
    const timestamp = new Date().getTime();
    await fetch(
      `${serveUrl}/msgSave/${messageTextEncoded}/${localStorage.getItem(
        "userId"
      )}/${timestamp}/true`,
      {
        method: "POST",
      }
    );

    getHistoy();
  };

  useEffect(() => {
    const socket = io(serveUrl);

    socket.on(`hideChat_${localStorage.getItem("userId")}`, async () => {
      try {
        window.location.reload();
      } catch (error: any) {
        console.error(error.message);
      }
    });

    const timer = setInterval(() => {
      getHistoy();
    }, 50000);

    return () => clearInterval(timer);
  });

  return {
    messages,
    sendMessage,
    isChatBanned,
  };
};

export default useChat;
