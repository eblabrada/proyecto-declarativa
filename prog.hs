import Control.Monad
import qualified Data.Sequence as Seq
import Data.Array
import Data.List
import Data.Maybe
import Data.Tuple (swap)
import Data.Foldable (toList)
import qualified Data.IntSet as Set
import qualified Data.ByteString as BS
import qualified Data.ByteString.Char8 as BS8
import Data.Bits (shiftL, (.&.), (.|.), xor, complementBit)
import Data.Array.IO
import Data.Array.MArray
import Control.Monad
import Data.IORef
import System.IO

getInt = read `fmap` getLine :: IO Int
getInts = (map (fst . fromJust . BS8.readInt) . BS8.words) `fmap` BS.getLine :: IO [Int]

findStart:: [[Int]] -> (Int, Int)
findStart a = head [(i, j) | i <- [0..length a - 1], j <- [0..length (a !! i) - 1], (a !! i) !! j == 1]

findObjects:: [[Int]] -> [(Int, Int)]
findObjects a = [(i, j) | i <- [0..length a - 1], j <- [0..length (a !! i) - 1], (a !! i) !! j == 2]

manhattanDistance:: (Int, Int) -> (Int, Int) -> Int
manhattanDistance (x1, y1) (x2, y2) = abs (x1 - x2) + abs (y1 - y2)

solve :: Int -> [(Int, Int)] -> IO (Int, [Int])
solve g garbagesWithStart = do
    let inf = 10^9
    dp <- newArray ((0, 0), (shiftL 1 g - 1, g - 1)) inf :: IO (IOUArray (Int, Int) Int)
    par <- newArray ((0, 0), (shiftL 1 g - 1, g - 1)) (-1) :: IO (IOUArray (Int, Int) Int)
    
    writeArray dp (1, 0) 0
    
    forM_ [0..shiftL 1 g - 1] $ \mask -> do
        forM_ [0..g-1] $ \i -> do
            isSet <- readArray dp (mask, i)
            when (isSet /= inf) $ do
                forM_ [0..g-1] $ \j -> do
                    let nmask = mask .|. shiftL 1 j
                    if mask .&. shiftL 1 j == 0
                        then do
                            let dist = manhattanDistance (garbagesWithStart !! i) (garbagesWithStart !! j)
                            oldDist <- readArray dp (nmask, j)
                            let newDist = isSet + dist
                            when (newDist < oldDist) $ do
                                writeArray dp (nmask, j) newDist
                                writeArray par (nmask, j) i
                        else return ()
    
    bestCost <- newIORef inf
    x <- newIORef (-1)
    let finalMask = shiftL 1 g - 1
    forM_ [1..g-1] $ \i -> do
        let dist = manhattanDistance (garbagesWithStart !! i) (garbagesWithStart !! 0)
        cost <- readArray dp (finalMask, i)
        best <- readIORef bestCost
        when ((cost + dist) < best) $ do
            writeIORef bestCost (cost + dist)
            writeIORef x i
    
    best <- readIORef bestCost
    -- putStrLn $ "Best Cost: " ++ show best

    path <- newIORef []
    let reconstructPath mask x = do
            when (mask /= 0) $ do
                modifyIORef path (x:)
                nx <- readArray par (mask, x)
                reconstructPath (mask .&. complementBit mask x) nx
    
    xVal <- readIORef x
    reconstructPath finalMask xVal
    finalPath <- readIORef path

    let finalPathRev = reverse finalPath

    return (best, finalPath)

main = do
    -- putStrLn "======================"
    -- putStrLn "Escriba la descripción del mapa:"
    -- putStrLn "  Dimensión del mapa"
    -- putStrLn "  0 - Casilla vacía"
    -- putStrLn "  1 - Casilla con el robot"
    -- putStrLn "  2 - Casilla con un objeto para recoger"
    -- putStrLn "Objetivo: Imprimir el mejor camino desde la posición del robot para recoger todos los objetos y volver a la posición inicial"
    -- putStrLn "======================"
    
    contents <- readFile "map.txt"
    let a = map (map read . words) (lines contents) :: [[Int]]
        n = length a
    
    let start = findStart a
        garbages = findObjects a
        garbagesWithStart = (start : garbages)
        g = length garbagesWithStart
    
    (best, finalPath) <- solve g garbagesWithStart

    -- Redirect output to path.txt
    withFile "path.txt" WriteMode $ \h -> do
        hPutStrLn h $ unwords [show (garbagesWithStart !! i) | i <- finalPath]