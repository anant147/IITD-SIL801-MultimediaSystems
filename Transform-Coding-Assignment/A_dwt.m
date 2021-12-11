% dwt transform (haar transform)

% reading image
B = imread('newImg.jpeg');
%imshow(B)

% converting rgb image to gray
C = rgb2gray(B);
%imshow(C)

[row,col,chan] = size(C);
disp(row)
disp(col)
disp(chan)

% Division of image to blocks (sub images)
row_ext = mod(row, 8);
col_ext = mod(col, 8);

% finding no. of rows and cols to be added 
if ne(row_ext,0)
   r = 8 - row_ext;
else
    r = 0;
end

if ne(col_ext,0)
    c = 8 - col_ext;
else
    c = 0;
end

% changing image by padding obtained value of r and c
D = padarray(C,[r c],0,'both');
[nrow,ncol,nchan] = size(D);
disp(nrow)
disp(ncol)
disp(nchan)

% making cell for storing subblock of 8*8
rb = nrow/8;
rc = ncol/8;

E = cell([rb rc]);

% filling value of slices of D into cells of E
for ri = 1:rb
    for ci = 1:rc
        rst = ((ri-1)*8)+1;
        red = ((ri-1)*8)+8;
        cst = ((ci-1)*8)+1;
        ced = ((ci-1)*8)+8;
        E{ri, ci} = round(D(rst:red, cst:ced));
    end
end

disp(E)

% Transform of blocks (haar transform)
F = cell([rb rc]);

for ri = 1:rb
    for ci = 1:rc
        [a,h,v,d] = haart2(E{ri,ci});
        temp = {a,h,v,d};
        F{ri,ci} = temp;
    end
end

disp(F)

% Inverse transform (haar transform)
I = cell([rb rc]);

for ri = 1:rb
    for ci = 1:rc
        a = F{ri,ci}{1,1};
        h = F{ri,ci}{1,2};
        v = F{ri,ci}{1,3};
        d = F{ri,ci}{1,4};
        I{ri, ci} = round(ihaart2(a,h,v,d));
    end
end

disp(I)

% Reconstruction of image 
J = zeros(nrow,ncol,'uint8');

for ri = 1:rb
    for ci = 1:rc
        for i = 1:8
            for j = 1:8
                rind = ((ri-1)*8)+i;
                cind = ((ci-1)*8)+j;
                J(rind, cind) = I{ri, ci}(i,j);
            end
        end
    end
end

disp(J)
imshow(J)

% Calculating error 
err = immse(C,J);
fprintf('\n The mean-squared dwt(haar) error is %f\n', err);



