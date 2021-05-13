---
author: YelloChunk
tags: Glibc_Resolve
---

## Chunk Range:

Tcache  0x20-0x410       LIFO         when FASTBIN stash into tcache will Reverse the List

FastBin: 0x20 - 0x80    	LIFO

SmallBin:0x20-0x3f0		First FIT

LargeBin: 0x400 < LargeBin < Mmap ThreShould         First FIT

UnsortedBin : None



## Malloc :

  Tcache   

  IF {FastBin

​	 		Check Idx.

​				stash Fastbin

​		}

  IF{SmallBin

​			 Double LinkList Check

​			  stash SmallBin

​		}

 ELSE IF{LargeBin

​	IF have fastbins  GOTO consolidate

START A LOOP

​	{

​		while(UNSORTED BIN EXISTS)

​		{

​			Check UnsortedBin 1.size and nextsize. 2 presize match 3 .DoubleLink 4.InuseBit

​					 IF NB IN SMALLBIN AND LAST REMAINDER

​							Split and reattch Remainder

​					IF NOT last remainder . 

​							But Exact Fit Try Put To Tcache First.

​					Nether LastRemainde Nor Exact Fit

​							Put Unsorted Into Where it should go

​									SmallBin Or LargeBin

​		}

​				Retry GetChunk From Bins

​							1.Directly From Large Bin   2. Use BinMap For Other.

​				When No Any Way . GOTO USE_TOP

​						use_top:

​								1.Check Top Size.  2. Size Enough Get Chunk Directly 

​								3.Not Enough Try Consolidate Fast Again 4. No anyway . sysmalloc()		

​	}																						

}		

## FREE:   Need Aligned Ptr

 	Tcache Put With EZ Double Free Check

​	  FASTBIN: SIZE CHECK  | NEXT SIZE CHECK |  DOUBLE FREE |  CHECK FIRST OLD SIZE

​	  Other Bin(Non Mmap): Consolidate. CHECK TOP | CHECK SIZE | 

​											CHECK NEXT INUSEBIT| NEXTSIZE CHECK 

​					Previous Consolidate . Check Size with Prev_Size

​					if(nextchunk!=TopChunk)

​							{

​								Next Consolidate  .  No more check.Just bypass Unlink & Next's Next inuse bit

​	  							Try Put into Unsorted Bin:

​									1.Double Link Check  2. Put into Unsorted Bin's Fd  3

​							}

​					else Consolidate into top

​					If size bigger than FASTBIN_CONSOLIDATION_THRESHOLD 

​									run malloc_consolidate(av)

​					

## Consolidate:

​	Consolidate Fastbin

{

​		From 0 To FastMax :  (DO THIS TO EVERY FASTBIN'S CHUNK)

​			Check FastSize

​					Then Try Phsical  ForWard And BackWard Chunk Consolidate.

​									Pre Chunk Check .PreSize = pre_size/ // Find By Prev

​									Next Chunk Check . Not Top.   Find By  Size Offset. Check Next Inuse Bit.

​					Put Consolidate Into Unsorted Bin														

​		 		IF NEXT IS TOP . Consolidate into Top

}

