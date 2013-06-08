===================
State System Layers
===================

The salt state system is comprised of multiple layers. While using Salt does
not require an understanding of the state layers a deeper understanding of
how Salt compiles and manages states can be very beneficial.

Function Call
=============

The lowest layer of functionality in the state system is the direct state
function call. Sate executions are executions of single state functions at
the core, these individual functions are defined in state modules and can
be called directly via the ``state.single`` command.

Low Chunk
=========

The low chunk is the bottom of the Salt state compiler. This is a data
representation of a single function call. The low chunk is sent to the state
caller and used to execute a single state function.

A single low chunk can be executed manually via the ``state.low`` command.

Low State
=========

High Data
=========

SLS
====

HighState
=========

OverState
=========
