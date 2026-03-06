import React, { useState, useRef } from 'react'
import {Chess, type Square } from  "chess.js"
import { Chessboard, type PieceDropHandlerArgs, type SquareHandlerArgs } from 'react-chessboard'

function App() {
  const chessGameRef = useRef(new Chess())
  const chessGame = chessGameRef.current
  

  const [chessPosition, setChessPosition] = useState(chessGame.fen())
  const [moveFrom, setMoveFrom] = useState("")
  const [optionSquares, setOptionSquares] = useState({})

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
  
  function getMoveOptions(square: Square){
    const moves = chessGame.moves({
        square,
        verbose: true
      });
    if (moves.length ===0){
      setOptionSquares({})
      return false
    }
    const newSquares : Record<string, React.CSSProperties> ={}
    for (const move of moves){
      newSquares[move.to] = {
        background: chessGame.get(move.to) && chessGame.get(move.to)?.color !== chessGame.get(square)?.color ? 'radial-gradient(circle, rgba(0,0,0,.1) 85%, transparent 85%)'
        : 'radial-gradient(circle, rgba(0,0,0,.1) 25%, transparent 25%)',
        // smaller circle for moving
          borderRadius: '50%'
      }
    }
    newSquares[square] = {
        background: 'rgba(255, 255, 0, 0.4)'
      };

      // set the option squares
      setOptionSquares(newSquares);

      // return true to indicate that there are move options
      return true;
  }

   function onSquareClick({
      square,
      piece
    }: SquareHandlerArgs) {
      // piece clicked to move
      if (!moveFrom && piece) {
        // get the move options for the square
        const hasMoveOptions = getMoveOptions(square as Square);

        // if move options, set the moveFrom to the square
        if (hasMoveOptions) {
          setMoveFrom(square);
        }

        // return early
        return;
      }

      // square clicked to move to, check if valid move
      const moves = chessGame.moves({
        square: moveFrom as Square,
        verbose: true
      });
      const foundMove = moves.find(m => m.from === moveFrom && m.to === square);

      // not a valid move
      if (!foundMove) {
        // check if clicked on new piece
        const hasMoveOptions = getMoveOptions(square as Square);

        // if new piece, setMoveFrom, otherwise clear moveFrom
        setMoveFrom(hasMoveOptions ? square : '');

        // return early
        return;
      }

      // is normal move
      try {
        chessGame.move({
          from: moveFrom,
          to: square,
          promotion: 'q'
        });
      } catch {
        // if invalid, setMoveFrom and getMoveOptions
        const hasMoveOptions = getMoveOptions(square as Square);

        // if new piece, setMoveFrom, otherwise clear moveFrom
        if (hasMoveOptions) {
          setMoveFrom(square);
        }

        // return early
        return;
      }

      // update the position state
      setChessPosition(chessGame.fen());

      // make random cpu move after a short delay
      setTimeout(makeRandomMove, 300);

      // clear moveFrom and optionSquares
      setMoveFrom('');
      setOptionSquares({});
    }







  const chessBoardOptions = {
    allowDragging: false,
    position: chessPosition,
    onPieceDrop,
    id: 'play-vs-random',
    onSquareClick,
          squareStyles: optionSquares,


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
