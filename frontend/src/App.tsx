import { useState, useRef } from 'react'
import {Chess } from  "chess.js"
import { Chessboard, type PieceDropHandlerArgs } from 'react-chessboard'

function App() {
  const chessGameRef = useRef(new Chess())
  const chessGame = chessGameRef.current

  const [chessPosition, setChessPosition] = useState(chessGame.fen())

  // random move Generator
  function makeRandomMove(){
    
    
    const possibleMoves = chessGame.moves()
    
    if(chessGame.isGameOver()){
      return
    }

    const ranadomMove = possibleMoves[Math.floor(Math.random()  * possibleMoves.length)]

    chessGame.move(ranadomMove)
    setChessPosition(chessGame.fen())
  }

  function onPieceDrop({sourceSquare,targetSquare} : PieceDropHandlerArgs){
    if(!targetSquare) return false
  
  try {
    chessGame.move({from:sourceSquare, to:targetSquare, promotion:"q"})
    setChessPosition(chessGame.fen())
    setTimeout(makeRandomMove, 500);
    return true
  }catch{
    return false
  }}
  const chessBoardOptions = {
    position: chessPosition,
    onPieceDrop,
    id: 'play-vs-random'
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen font-sans text-white">
      <div className="w-full max-w-[500px] px-4">
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-100">
                    مبروك لك الشرف بتلعب مع بوت اللورد محمد☕، ان شاء الله اذا صرت شخص كفو بيفضي لك محمد ربع ساعة من وقته ويلعب معك

        </h1>
        
        <div className="shadow-2xl rounded-lg overflow-hidden border-4 border-gray-700">
          <Chessboard 
            options={chessBoardOptions}
          />
        </div>
      </div>
    </div>
  )
}

export default App
