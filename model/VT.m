
%Voronoi
[V,C] = voronoin([xx,yy]);
%可视化
for i = 1:length(C)
	if all(C{i}~=1)   % If at least one of the indices is 1,
                  % then it is an open region and we can't
                  % patch that.
		Verts = V(C{i},:);
		CoordAbs = abs(Verts(:));
		if all(CoordAbs <= 1+eps(single(1)))%within boundary
			patch(V(C{i},1),V(C{i},2),i); % use color i.
		end
	end
end
view(2)

%2、生成各点坐标
f=fullfile('C:','temp','grain_topology_coords.txt');
fileID = fopen(f,'w');
[mmm,nnn]=size(V);
fprintf(fileID,'%f,%f\n',10000,10000);
for i=2:mmm
	fprintf(fileID,'%f,%f\n',V(i,1), V(i,2));
end
fclose(fileID);

%3、生成各晶粒顶点连接顺序
f=fullfile('C:','temp','grain_topology_connection.txt');
fileID = fopen(f,'w');
for i=1:s
	for j=1:size(C{i,:})
		fprintf(fileID,'%d,',C{i,j});
	end
	fprintf(fileID,'\n');
end
fclose(fileID);

%4、输出voronoi核心
f=fullfile('C:','temp','grain_nucleus.txt');
fp=fopen(f,'w');
for i=1:s
   fprintf(fp, '%f,%f,%f\n', x(i), y(i), 0);
end
fclose(fp);