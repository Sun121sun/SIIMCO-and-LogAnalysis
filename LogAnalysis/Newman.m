clear all
close all
clc
 
% load preprocess.mat
% E=e;

A = cell2mat(struct2cell(load('email.mat')));

E=A;
% E(find(E>0))=1;%�����ڽӾ���
tic;
e=E;
e(e==1)=1/sum(E(:));
a=sum(e);
n=size(A,2);
b=[1:n];
b=num2cell(b);%�����洢����Ԫ�صı���
c={};
k=1;
while length(e)>1
      lg=length(e);
      detaQ=-(10^9)*ones(n-k+1);%��Q
      for i=1:lg-1
          for j=i+1:lg
             if e(i,j)~=0
                detaQ(i,j)=2*(e(i,j)-a(i)*a(j));%�����Q
             end
          end
      end
   if sum(detaQ+(10^9))==0
      break
   end
% Q(k)=max(detaQ(:));%Ѱ�ҡ�Q�����ֵ���������洢��Q(k)����
%-----------------------------Ѱ������Q��Ӧ���������ţ�������ϲ������ı�e����
[I,J]=find(detaQ==max(detaQ(:)));
 
     for ii=1:length(I)
         e(J(ii),:)=e(I(ii),:)+e(J(ii),:);
         e(I(ii),:)=0;
         e(:,J(ii))=e(:,I(ii))+e(:,J(ii));
         e(:,I(ii))=0;
 
% e(I,I)=e(I,I)/2;
%��������������������¼��Q�������Ӧ�������Լ��������е�Ԫ��
 
        b{J(ii)}=[b{I(ii)} b{J(ii)}];
        b{I(ii)}=0;
     end
 
  e(I,:)=[];
  e(:,I)=[];
  b(I)=[];
  c(k,:)=num2cell(zeros(1,n));
  c(k,1:length(b))=b;
  for kk=1:length(b)
      c2=cell2mat(c(k,kk));
      c2(c2==0)=[];
      c{k,kk}=c2;
      c2=[];
  end
a=sum(e);
k=k+1;
tmp=0;
  for jj=1:length(e)
      tmp=tmp+(e(jj,jj)-a(jj)*a(jj));
  end
Q(k)=tmp;
end
max_k=find(Q==max(Q(:)))-1;
 
ll=0;
for i=1:length(c(max_k,:))
    if sum(c{max_k,i})~=0
        ll=ll+1;
        c{max_k,i}=c{max_k,i}(c{max_k,i}~=0);
    end
end
c_newman=c(max_k,1:ll);
save result c_newman
label=zeros(n,1);
for i=1:ll
    label(c{max_k,i}')=i;
end