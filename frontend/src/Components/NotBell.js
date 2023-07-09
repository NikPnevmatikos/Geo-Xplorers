import React, { useContext} from 'react';

import MagicBell, {
    FloatingNotificationInbox,
  } from "@magicbell/magicbell-react";

  import "../Styles/Not.css";

  import { UserContext } from '../App';

  export default function NotBell() {
    const [user, setUser] = useContext(UserContext);
    return (
        <div magicbell-container>
             <div className="notification-inbox-container">
      <MagicBell
        apiKey="f6418835e896ef955a25dba107cce5f5bafe06a5"
        userEmail="xplorersgeo@gmail.com"
        theme={theme}
        locale="en"
        bellCounter="unread"
        userExternalId= {`Bearer ${user.token}`}
        userKey={`Bearer ${user.token}`}
      >
        {(props) => (
          <FloatingNotificationInbox
            width={450}
            height={500}
            {...props}
            layout={["header", "content"]}
          />
        )}
      </MagicBell>
      </div>
      </div>
    );
  }
  const theme = {
    header: {
      fontFamily: "inherit",
    //   backgroundColor: "rgb(99, 161, 171, 1)",
      textColor:  "rgb(99, 161, 171, 1)",
      fontSize: "17px",
      borderRadius: "9px",
    },
    notification: {
      default: {
        fontSize: "14px",
        borderRadius: "9px",
        margin: "8px",
        backgroundColor: "#FFFFFF",
        textColor: "#3A424D",
        fontFamily: "inherit",
        hover: { backgroundColor: "#d8d9d9" }
      },
      unread: {
        backgroundColor: " #f1f3f4",
        textColor: "#3A424D",
        hover: { backgroundColor: "#d8d9d9" },
        state: { color: "rgb(99, 161, 171, 1)" },
      },
      unseen: {
        backgroundColor: "#F8F5FF",
        textColor: "#3A424D",
        hover: { backgroundColor: "#d8d9d9" },
        state: { color: "#5225C1" },
      },
    },
    icon: { borderColor: "#f1f3f4", width: "27px" },
    unseenBadge: { backgroundColor: "rgb(99, 161, 171, 1)" },
    banner: {
      backgroundColor: "#F8F5FF",
      textColor: "#3A424D",
      fontSize: "14px",
    },
    dialog: {
      backgroundColor: "#F5F5F5",
      textColor: "#313131",
      accentColor: "#5225C1",
    },
  };