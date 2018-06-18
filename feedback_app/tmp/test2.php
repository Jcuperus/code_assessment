<?php

class Message
{
    $message

    public function __construct($message) 
    {
        $this->message = $message
    }

    public function printMessage()
    {
        echo "Message " + $this->message
    }
}