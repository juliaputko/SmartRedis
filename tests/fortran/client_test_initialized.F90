! BSD 2-Clause License
!
! Copyright (c) 2021-2023, Hewlett Packard Enterprise
! All rights reserved.
!
! Redistribution and use in source and binary forms, with or without
! modification, are permitted provided that the following conditions are met:
!
! 1. Redistributions of source code must retain the above copyright notice, this
!    list of conditions and the following disclaimer.
!
! 2. Redistributions in binary form must reproduce the above copyright notice,
!    this list of conditions and the following disclaimer in the documentation
!    and/or other materials provided with the distribution.
!
! THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
! AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
! IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
! DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
! FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
! DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
! SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
! CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
! OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
! OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

program main
  use smartredis_client, only : client_type
  use test_utils, only : use_cluster
  use iso_fortran_env, only : STDERR => error_unit
  use iso_fortran_env, only : STDOUT => output_unit
  use iso_c_binding, only : c_ptr, c_bool, c_null_ptr, c_char, c_int
  use iso_c_binding, only : c_int8_t, c_int16_t, c_int32_t, c_int64_t, c_float, c_double, c_size_t

  implicit none

#include "enum_fortran.inc"

  type(client_type) :: client
  integer :: result
  character(kind=c_char, len=:), allocatable :: client_str

  if (client%isinitialized()) error stop 'client not initialized'

  result = client%initialize("client_test_initialized")
  if (result .ne. SRNoError) error stop

  if (.not. client%isinitialized()) error stop 'client is initialized'

  client_str = client%to_string()
  if (client_str(1:6) .ne. "Client") error stop
  write(*,*) client_str

  call client%print_client()
  call client%print_client(STDOUT)

  write(*,*) "client initialized: passed"

end program main
