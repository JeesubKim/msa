import React, { useState, useEffect } from "react";
import axios from "axios";

const CommentList = ({ comments }) => {
  const renderedComments = comments.map((comment) => {
    let content = "";
    const status = comment["status"];
    if (status === "approved") {
      content = comment["content"];
    } else if (status === "pending") {
      content = "This comment is awaiting moderation";
    } else if (status === "rejected") {
      content = "This comment has been rejected";
    }
    return <li key={comment.id}>{content}</li>;
  });

  return <ul>{renderedComments}</ul>;
};

export default CommentList;
