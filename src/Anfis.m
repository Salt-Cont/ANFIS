function out = Anfis(data)
Opt = genfisOptions('GridPartition')
Opt.NumMembershipFunctions = 3
Opt.InputMembershipFunctionType = 'gaussmf'
out = evalfis(anfis(data,anfisOptions('InitialFIS',genfis(data(:,1:3), data(:,4),Opt), 'Epochnumber',1000)),data(:,1:3))
end