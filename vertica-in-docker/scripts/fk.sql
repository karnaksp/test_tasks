-- Внешние ключи --

ALTER TABLE RgdDivisDprt
ADD CONSTRAINT fk_RgdCode_Class305_Code FOREIGN KEY (Class305_Code) REFERENCES Class305 (Class305_Code);

ALTER TABLE public.CliTurnoverDtl
ADD CONSTRAINT fk_CliCode_DescKontrag FOREIGN KEY (CliCode) REFERENCES DescKontrag (CliCode);

ALTER TABLE public.CliTurnoverDtl
ADD CONSTRAINT fk_RgdCode_RgdDivisDprt FOREIGN KEY (RgdCode) REFERENCES RgdDivisDprt (RgdCode);

ALTER TABLE public.CliTurnoverDtl
ADD CONSTRAINT fk_Class37_Code_Class37 FOREIGN KEY (Class37_Code) REFERENCES Class37 (Class37_Code);