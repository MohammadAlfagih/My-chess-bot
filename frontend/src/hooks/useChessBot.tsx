import { useState, useEffect, useRef, useCallback } from "react";

interface BotResponse {
  status: string;
  move: string;
  fen:string

}


export function useChessBot(botcolor: 'w' | "b"){
    const [isConnected, setIsConnected] = useState(false)
    const [botMove, setBotMove] = useState<string | null>(null)
    const wsRef = useRef<WebSocket  | null>(null)

    useEffect(() => {
        const ws = new WebSocket("ws://127.0.0.1:8000/ws/play")
        wsRef.current = ws
        ws.onopen = () => setIsConnected(true)
        ws.onclose = () => setIsConnected(false)

        ws.onmessage = (event) =>{
            const data : BotResponse = JSON.parse(event.data)
            if(data.status === "success"){
                setBotMove(data.move)
            }
        }
        return () => {
            ws.close()
        }
    },[])
    const sendPosition = useCallback((fen: string) => {
        if(wsRef.current && wsRef.current.readyState === WebSocket.OPEN){
            setBotMove(null)
            wsRef.current.send(JSON.stringify({fen, bot_color: botcolor}))
        }else{
            console.warn("no connction yet")
        }
    }, [botcolor])
    return {isConnected,botMove,sendPosition,setBotMove}

}
