/*
 FUNCTION:
   dbo.CONDEL
 CREATED:
   20240918
 AUTHOR:
   github/silarin
 PURPOSE:
   Using SQL to simulate the conDel() X++ container function. This builds on the CONPEEK() and CONSIZE() SQL functions created by Cody Thimm.
   I found a need to extract data from very large containers in Dynamics AX. However the CONPEEK function has a limitation with its VARBINARY(8000) parameter.
   The workaround is to delete a container from the main container, and then use CONPEEK to extract the data.
   Looping within the 8k limit allows CONPEEK to extract any container data without hanging up.
 PARAMETERS:
   varbinary(max), -- the container to delete from
   int -- which container to delete
 RETURN:
   varbinary(max) -- the resulting container after deleting
 */
CREATE FUNCTION [dbo].[CONDEL] (@bin AS VARBINARY(MAX), @i AS INT)
RETURNS VARBINARY(MAX)
AS
  BEGIN
  	DECLARE @ret AS VARBINARY(MAX);
  	SET @ret = CAST(STUFF(
  					@bin -- data
  					,CHARINDEX(CAST(dbo.CONPEEK(@bin,@i) AS VARBINARY(MAX)),@bin) -- start pos
  					,dbo.CONSIZE(CAST(dbo.CONPEEK(@bin,@i) AS VARBINARY(MAX)))+1 -- length
  					,0x -- replace
  				) AS VARBINARY(MAX))
  	RETURN @ret
  END
GO
