mainDir = '/home/jmmauricio/Documents/APEIRON2012/Iturri/EnsayosBateria'
testDir = 'Descarga1'

lsDir=dir([mainDir '/' testDir '/'])


M=[];
for it =1:size(lsDir,1)-14
    disp(it)
    M=[M; csvread([mainDir '/' testDir '/' lsDir(it+2).name])];
end
    
 

t_0=M(1,1);

T=[M(:,1)]-t_0;
V=[M(:,2)]*3.3/3.32;
I=[M(:,3)];
SOC=[M(:,4)];

figure
Nbat=round(350/3.3);
n_ini = min(find(T>50))
n_end = min(find(T>330))
F0=fit(-I(n_ini:n_end),Nbat*V(n_ini:n_end), 'poly1')
plot(-I(n_ini:n_end),Nbat*V(n_ini:n_end),'x', 'LineWidth', 2)
hold on
I_extra = -120:10:120;
plot(I_extra,F0.p1*I_extra+F0.p2, 'g', 'LineWidth', 2)
hold on
plot(I_extra,(I_extra-I_extra)+380, 'r', 'LineWidth', 2)
plot(I_extra,(I_extra-I_extra)+310, 'r', 'LineWidth', 2)
plot(I_extra,(I_extra-I_extra)+3.3*Nbat, 'b', 'LineWidth', 2)

grid
ylim([280,420])
xlim([-120,120])
xlabel('Corriente (A)'); 
ylabel('Tension (V)'); 
set(gcf,'Name',' Nombre de la figura ') % Opcional
set(gcf,'Color',[1 1 1])
print('-depsc', '-r400',  '-adobecset', ['test_1_i_v'  ])
unix(['epstopdf '    'test_1_i_v'  '.eps' ])
  
  
%%
figure
 subplot(3,1,1), plot(T,I)
 ylabel('Corriente (A)'); 
 grid
 subplot(3,1,2), plot(T,V)
 ylabel('Tension (V)'); 
 grid
 subplot(3,1,3), plot(T,SOC/40)
 ylabel('SOC (V)'); 
 grid
 xlabel('Tiempo (s)'); 

set(gcf,'Name',' Nombre de la figura ') % Opcional
set(gcf,'Color',[1 1 1])
print('-depsc', '-r400',  '-adobecset', ['test_1_t_i_t_v'  ])
unix(['epstopdf '    'test_1_t_v'  '.eps' ])
 