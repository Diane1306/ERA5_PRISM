PROGRAM MAIN
!    character*300 :: input,output1,output2
	REAL, DIMENSION(0:356) :: lat
	REAL, DIMENSION(0:721) :: lon
    character*300 inputfile
    
	
	do i = 0, 356
		lat(i) = 49.91666667 - i * 0.0416666666667
	end do
!	write(*,*)lat
	
	do i = 0, 721
		lon(i) = -105.04166667 + i * 0.0416666666667
	end do
!	write(*,*)lon
!	write(*,'(A,F5.2)')'A',2.12345
    
    OPEN(1,FILE='input_list.txt',STATUS='OLD')
    do i = 1, 10
        read(1, *)inputfile
        write(*,*)inputfile
    end do
    CLOSE(1, STATUS='KEEP') 
    
		
end program
