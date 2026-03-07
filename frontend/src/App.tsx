import React, { useState, useRef, useEffect } from "react";
import { Chess, type Square } from "chess.js";
import {
  Chessboard,
  type PieceDropHandlerArgs,
  type SquareHandlerArgs,
} from "react-chessboard";
import { useChessBot } from "./hooks/useChessBot";

function App() {
  const chessGameRef = useRef(new Chess());
  const [chessPosition, setChessPosition] = useState(() => new Chess().fen());
  const [resetCount, setResetCount] = useState(0)
  const [moveFrom, setMoveFrom] = useState("");
  const [optionSquares, setOptionSquares] = useState({});
  const [botColor, setBotColor] = useState<"w" | "b">("b");
  const { isConnected, botMove, sendPosition, setBotMove } =
    useChessBot(botColor);
  const [boardOrientation, setBoardOrientation] = useState<"white" | "black">(
    "white",
  );

  useEffect(() => {
    if (botMove) {
      const chessGame = chessGameRef.current;

      try {
        const from = botMove.substring(0, 2);
        const to = botMove.substring(2, 4);
        const promotion = botMove.length > 4 ? botMove[4] : "q";
        chessGame.move({ from, to, promotion });
        setChessPosition(chessGame.fen());
        setBotMove(null);
      } catch (e) {
        console.error("error happend", e);
      }
    }
  }, [botMove, setBotMove]);
  //if bot is white
  useEffect(() => {
    const chessGame = chessGameRef.current;

    if (isConnected && botColor === "w" && chessGame.history().length === 0) {
      sendPosition(chessGame.fen());
    }
  }, [isConnected, botColor, sendPosition,resetCount]);

  // random move Generator
  // function makeRandomMove(){

  //   const possibleMoves = chessGame.moves()

  //   if(chessGame.isGameOver()){
  //     return
  //   }

  //   const ranadomMove = possibleMoves[Math.floor(Math.random()  * possibleMoves.length)]

  //   chessGame.move(ranadomMove)
  //   setChessPosition(chessGame.fen())
  // }

  function onPieceDrop({ sourceSquare, targetSquare }: PieceDropHandlerArgs) {
    const chessGame = chessGameRef.current;
    if (!targetSquare) return false;

    try {
      chessGame.move({ from: sourceSquare, to: targetSquare, promotion: "q" });
      setChessPosition(chessGame.fen());
      sendPosition(chessGame.fen());
      return true;
    } catch {
      return false;
    }
  }

  function getMoveOptions(square: Square) {
    const chessGame = chessGameRef.current;

    const moves = chessGame.moves({
      square,
      verbose: true,
    });
    if (moves.length === 0) {
      setOptionSquares({});
      return false;
    }
    const newSquares: Record<string, React.CSSProperties> = {};
    for (const move of moves) {
      newSquares[move.to] = {
        background:
          chessGame.get(move.to) &&
          chessGame.get(move.to)?.color !== chessGame.get(square)?.color
            ? "radial-gradient(circle, rgba(0,0,0,.1) 85%, transparent 85%)"
            : "radial-gradient(circle, rgba(0,0,0,.1) 25%, transparent 25%)",
        // smaller circle for moving
        borderRadius: "50%",
      };
    }
    newSquares[square] = {
      background: "rgba(255, 255, 0, 0.4)",
    };

    // set the option squares
    setOptionSquares(newSquares);

    // return true to indicate that there are move options
    return true;
  }

  function onSquareClick({ square, piece }: SquareHandlerArgs) {
    const chessGame = chessGameRef.current;

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
      verbose: true,
    });
    const foundMove = moves.find((m) => m.from === moveFrom && m.to === square);

    // not a valid move
    if (!foundMove) {
      // check if clicked on new piece
      const hasMoveOptions = getMoveOptions(square as Square);

      // if new piece, setMoveFrom, otherwise clear moveFrom
      setMoveFrom(hasMoveOptions ? square : "");

      // return early
      return;
    }

    // is normal move
    try {
      chessGame.move({
        from: moveFrom,
        to: square,
        promotion: "q",
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
    sendPosition(chessGame.fen());

    // clear moveFrom and optionSquares
    setMoveFrom("");
    setOptionSquares({});
  }

  const chessBoardOptions = {
    allowDragging: true,
    position: chessPosition,
    onPieceDrop,
    id: "play-vs-Mo7asbot",
    onSquareClick,
    squareStyles: optionSquares,
    boardOrientation: boardOrientation,
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen font-sans text-white">
      <div className="w-full max-w-[500px] px-4">
        <p className="font-bold text-center mb-6 text-gray-100">
          مبروك لك الشرف بتلعب مع بوت اللورد محمد☕، ان شاء الله اذا صرت شخص كفو
          بيفضي لك محمد ربع ساعة من وقته ويلعب معك
        </p>

        <div className="shadow-2xl rounded-lg overflow-hidden border-4 border-gray-700">
          <Chessboard options={chessBoardOptions} />
        </div>
        <div className="flex justify-center gap-4 mt-8">

        
        <button
          onClick={() => {
            chessGameRef.current.reset();
            setChessPosition(chessGameRef.current.fen());
            setBotColor("w");
            setBoardOrientation("black");
            setResetCount(c => c+1)
          }}
          className="px-6 py-3 bg-gray-800 hover:bg-gray-700 hover:cursor-pointer text-white font-semibold rounded-lg shadow-md transition duration-200 ease-in-out border border-gray-600 w-1/2"

        >
          Play as black
        </button>
        <button
          onClick={() => {
            chessGameRef.current.reset();
            setChessPosition(chessGameRef.current.fen());
            setBotColor("b");
            setBoardOrientation("white");
            setResetCount(c => c+1)
          }}
          className="px-6 py-3 bg-gray-100 hover:cursor-pointer hover:bg-gray-300 text-gray-900 font-semibold rounded-lg shadow-md transition duration-200 ease-in-out w-1/2"
        >
          Play as White
        </button>
        </div>
      </div>
    </div>
  );
}

export default App;
