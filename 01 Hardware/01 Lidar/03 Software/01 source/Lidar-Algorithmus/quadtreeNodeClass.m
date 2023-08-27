% Autor: Thach
% Verwendungszweck: Modellierung eines Nodes vom Quadtree
% Erstellt am 14.08.2023
% Version: 1.00
% Revision: 1.08

classdef quadtreeNodeClass < handle
    properties (Access = public)
        pointsList = []%das Array für die Punktepositionen in X und Y
        child = 0
    end
    properties (GetAccess = public, SetAccess=private)
        %Bot- und Top-Punkt
        %Bot
        xValMin{mustBeNumeric}
        yValMin{mustBeNumeric}
        %Top
        xValMax{mustBeNumeric}
        yValMax{mustBeNumeric}

        %Position in der Quadtree-Stufe
        level{mustBeNumeric}
        %Die Name - nur zum Betrachten
        name
        %Init-Flag
        init = false
        %Klasse-ID
        id = 2
    end

    methods (Access=private)
        function []=sortPointsListX(obj)
            %Aufnahme aller X-Werte
            temp = cellfun(@(x)x(1,1),obj.pointsList);
            % betrachtet nur 2.Ausgabe
            [~,sortedIndex] = sort(temp);
            % Wiederordnung in abhängig von der neuen Indexanordnung
            obj.pointsList = obj.pointsList(sortedIndex);
        end

        function []=sortPointsListY(obj)
            %Aufnahme aller X-Werte
            temp = cellfun(@(x)x(1,2),obj.pointsList);
            % betrachtet nur 2.Ausgabe
            [~,sortedIndex] = sort(temp);
            % Wiederordnung in abhängig von der neuen Indexanordnung
            obj.pointsList = obj.pointsList(sortedIndex);
        end

        function indexArrayVal=searchPoint(obj,x,y)
            if nargin~=3
                error('nicht genug Parameter für Funktion');
            elseif isempty(obj) || (obj.id~=2)
                error('Eingabe ist nicht gültig');
            elseif isempty(x) || isempty(y)
                error('Eingabe ist nicht gültig');
            else
                temp=zeros(1,numel(obj.pointsList));
                tempIndex=1;
                for i=1:numel(obj.pointsList)
                    coord = obj.pointsList{1,i};
                    if (coord(1,1) == x) && (coord(1,2) == y)
                        temp(1,tempIndex) = i;
                        tempIndex = tempIndex+1;
                    end
                end

                if(tempIndex~=1)
                    indexArrayVal = temp(1,1:(tempIndex-1));
                else
                    indexArrayVal=[];
                end
            end
        end

    end

    methods (Access=public)
        function obj=quadNodeInit(obj,bot,top)
            if nargin~=3
                error('Anzahl von Parametern für Konstruktor ungültig');
            elseif isempty(bot)||isempty(top)||isempty(obj)
                error('Eingabe ist nicht gültig');
            else
                xCmp = numCmp(top(1),bot(1));
                yCmp = numCmp(top(2),bot(2));
                if xCmp == 1 && yCmp == 1
                    obj.xValMax = top(1);
                    obj.yValMax = top(2);
                    obj.xValMin = bot(1);
                    obj.yValMin = bot(2);
                    obj.init = true;
                else
                    error('Eingabe ist nicht gültig');
                end
            end
        end

        function obj=setLevel(obj,level)
            if nargin~=2
                error('Anzahl von Parametern für Konstruktor ungültig');
            elseif isempty(level)||isempty(obj)
                error('Eingabe ist nicht gültig');
            else
                obj.level = level;
            end
        end

        function obj=setName(obj,name)
            if nargin~=2
                error('Anzahl von Parametern für Konstruktor ungültig');
            elseif isempty(name)||isempty(obj)
                error('Eingabe ist nicht gültig');
            else
                mustBeTextScalar(name);
                obj.name = name;
            end
        end

        function []=addAPoint(obj,input)
            if nargin~=2
                error('nicht genug Parameter für Funktion');
            elseif isempty(input) || ~isnumeric(input) || numel(input)~=2
                error('Eingabe nicht gültig');
            elseif isempty(obj) || (obj.id~=2)
                error('Eingabe nicht gültig');
            else
                obj.pointsList{numel(obj.pointsList)+1}= input;
            end
        end
        
        function arrayVal=removePointIdx(obj,index)
            if isempty(obj) || (obj.id~=2)
                error('Eingabe nicht gültig');
            elseif ~isnumeric(index) || ( ...
                    index > numel(obj.pointsList)) || (index<1)
                error('Eingabe nicht gültig');
            elseif isempty(index)
                arrayVal = [];
                obj.pointsList = [];
            else
                arrayVal = obj.pointsList{1,index};
                temp1=obj.pointsList(1,1:index-1);
                temp2=obj.pointsList(1,index+1:end);
                obj.pointsList=[temp1 temp2];%TODO optimiert es
            end
        end

        function arrayVal=removePointCoord(obj,x,y)
            if nargin~=3
                error('nicht genug Parameter für Funktion');
            elseif isempty(obj) || (obj.id~=2)
                error('Eingabe nicht gültig');
            elseif ~isnumeric(x) || ~isnumeric(y)
                error('Eingabe nicht gültig');
            else
                arrayVal=[];
                tempIndexArray = obj.searchPoint(x,y);
                if ~isempty(tempIndexArray)
                    temp=repmat({zeros(1,2)},1,numel(obj.pointsList));
                    tempIndex=0;
                    for i=1:numel(tempIndexArray)
                        %nach jeder Entfernung wird das nächste Index um 1 reduziert
                        tempIndexArray(1,i)=tempIndexArray(1,i)-tempIndex;
                        temp{1,i} = obj.removePointIdx(tempIndexArray(1,i));
                        tempIndex=tempIndex+1;
                    end
                    if tempIndex~=0
                        arrayVal = temp(1,1:tempIndex);
                    end
                end
            end
        end

        function []=sortPointsList(obj,coordinate)
            if nargin~=2
                error('Eingabe nicht gültig');
            elseif obj.id ~=2
                error('Eingabe nicht gültig');
            elseif isempty(obj.pointsList)
                error('Punktenlist ist leer');
            else
                switch coordinate
                    case 'x'
                        obj.sortPointsListX();
                    case 'y'
                        obj.sortPointsListY();
                    case 'xy'
                        %TODO Implementation noch in Bearbeitung
                        obj.sortPointsListX();
                    case 'yx'
                        %TODO Implementation noch in Bearbeitung
                        obj.sortPointsListY();
                    otherwise
                        error('Eingabe nicht gültig');
                end
            end
        end

    end
end