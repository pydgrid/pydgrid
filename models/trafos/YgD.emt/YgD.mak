
#------------------------------------------------------------------------------
# Project 'YgD' make using the 'gnu' compiler.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# All project
#------------------------------------------------------------------------------

all: targets
	@echo !--Make: succeeded.



#------------------------------------------------------------------------------
# Directories, Architecture, and Version
#------------------------------------------------------------------------------

Arch        = windows
EmtdcDir    = C:\PROGRA~1\PSCAD4~1\emtdc\gnu
EmtdcInc    = $(EmtdcDir)\inc
EmtdcBin    = $(EmtdcDir)\$(Arch)
EmtdcMain   = $(EmtdcBin)\main.obj
EmtdcLib    = $(EmtdcBin)\emtdc.lib


#------------------------------------------------------------------------------
# Fortran Compiler
#------------------------------------------------------------------------------

FC_Name     = f2c.exe
FC_Suffix   = o
FC_Args     = -r8 -w -Nn5000 -NL400 -Nx400
FC_Debug    =  -g
FC_Warn     = 
FC_Checks   = 
FC_Includes = -I"$(EmtdcInc)" -I"$(EmtdcBin)"
FC_Compile  = $(FC_Name) $(FC_Args) $(FC_Includes) $(FC_Debug) $(FC_Warn) $(FC_Checks)

#------------------------------------------------------------------------------
# C Compiler
#------------------------------------------------------------------------------

CC_Name     = gcc.exe
CC_Suffix   = o
CC_Args     = -c
CC_Debug    =  -O
CC_Includes = -I"$(EmtdcInc)" -I"$(EmtdcBin)"
CC_Compile  = $(CC_Name) $(CC_Args) $(CC_Includes) $(CC_Debug)

#------------------------------------------------------------------------------
# Linker
#------------------------------------------------------------------------------

Link_Name   = gcc.exe
Link_Debug  = 
Link_Args   = -o $@
Link        = $(Link_Name) $(Link_Args) $(Link_Debug)

#------------------------------------------------------------------------------
# Build rules for PSCAD generated files
#------------------------------------------------------------------------------


%.$(FC_Suffix): %.f
	@echo !--Compile: $<
	$(FC_Compile) $<
	$(CC_Compile) $*.c
	del $*.c


%.$(CC_Suffix): %.c
	@echo !--Compile: $<
	$(CC_Compile) $<



#------------------------------------------------------------------------------
# Build rules for file references
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
# Dependencies
#------------------------------------------------------------------------------


FC_Objects = \
 Main.$(FC_Suffix)

CC_Objects =

UserLibs =

SysLibs  = $(EmtdcBin)\libwsock32.a $(EmtdcBin)\libf2c.lib

Binary   = YgD.exe

$(Binary): $(FC_Objects) $(CC_Objects) $(UserLibs)
	@echo !--Link: $@
	$(Link) "$(EmtdcMain)" $(FC_Objects) $(CC_Objects) $(UserLibs) "$(EmtdcLib)" $(SysLibs)

targets: $(Binary)


clean:
	-del EMTDC_V*
	-del *.obj
	-del *.o
	-del *.exe
	@echo !--Make clean: succeeded.



