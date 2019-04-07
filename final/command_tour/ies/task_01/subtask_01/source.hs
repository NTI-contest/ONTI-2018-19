module Main where
 
import System.Environment
import System.IO
import Data.Ord
import Data.List
 
testFile = "/home/user/ips2019/sampleData.txt”
 
main :: IO ()
main = do
  h <- openFile testFile ReadMode
  hSetEncoding h utf8
  contents <- hGetContents h
  let loglines = tail . lines $ contents
  let grs = map readOneLine loglines
  print grs
  print $ findBest grs
  --print $ searchBest 10 ( metrics grs ) [] $ allCombs 5 10
 
data Gr = Gr
  { sun
  , sunGen :: Float
  } deriving ( Show )
 
readOneLine :: String -> Gr
readOneLine str = Gr w wg
  where
  (_:_:w:wg:_) = map read $ words str
 
data LC = LC [ Float ]
  deriving ( Show )
 
rlc ( LC x ) = LC ( reverse x )
 
theoreticDiff :: [ Gr ] -> LC -> Maybe Float
theoreticDiff grs (LC lcs)
  | length grs < length lcs = Nothing
  | otherwise = Just $ (^2) $ sum sunny - sunGen ( last grs )
  where
  pairs = zip grs $ reverse lcs
  ony ( gr, coeff ) = sun gr * coeff
  sunny = map ony pairs
 
metrics :: [ Gr ] -> LC -> Float
metrics [] _ = 0
metrics grs lc = case theoreticDiff grs lc of
  Nothing -> 0
  Just val -> val + metrics ( tail grs ) lc
 
allCombs :: Int -> Int -> [ LC ]
allCombs len steps = map LC $ map normalize $ sequence $ replicate len list
  where
  normalize :: [ Float ] -> [ Float ]
  normalize fs | sum fs == 0 = fs
               | otherwise = map (/ sum fs ) fs
  list = map fromIntegral [0..steps-1]
 
findBest :: [ Gr ] -> LC
findBest grs = minimumBy ( comparing ( metrics grs )) $ allCombs 10 3
 
searchBest :: Int -> ( a -> Float ) -> [ a ] -> [ a ] -> [ a ]
searchBest _ _ accum [] = accum
searchBest limit f accum (lc:lcs)
  | length accum < limit = searchBest limit f (lc:accum) lcs
  | otherwise = searchBest limit f ( tail $ sortBy ( comparing f ) (lc:accum)) lcs
