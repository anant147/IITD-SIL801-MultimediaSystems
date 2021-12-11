
% dct transform

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

% Transform of blocks
F = cell([rb rc]);

for ri = 1:rb
    for ci = 1:rc
        F{ri,ci} = round(dct2(E{ri,ci}));
    end
end

disp(F)

% Truncation or quantization (can try different strategies).
q_mtx = [16 11 10 16 24 40 51 61;
         12 12 14 19 26 58 60 55;
         14 13 16 24 40 57 69 56;
         14 17 22 29 51 87 80 62;
         18 22 37 56 68 109 103 77;
         24 35 55 64 81 104 113 92;
         49 64 78 87 103 121 120 101;
         72 92 95 98 112 100 103 99];

q_mtx = double(q_mtx);

G = cell([rb rc]);

for ri = 1:rb
    for ci = 1:rc
        G{ri, ci} = round(F{ri, ci} ./ q_mtx);
    end
end

disp(G)

% Dequantization 
H = cell([rb rc]);

for ri = 1:rb
    for ci = 1:rc
        H{ri, ci} = round(G{ri, ci} .* q_mtx);
    end
end

disp(H)

% Inverse transform
I = cell([rb rc]);

for ri = 1:rb
    for ci = 1:rc
        I{ri, ci} = round(idct2(H{ri,ci}));
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
fprintf('\n The mean-squared dct error is %f\n', err);



