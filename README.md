# npx-sample
Sample Form N-PX repo for sharing.

## Folders
- `sample_data` - raw and parsed forms
- `prompts` - initial prompt experiments

## Form N-PX document structure
1. Document header

Always present
```
<SEC-DOCUMENT>0001493580-21-000078.txt : 20210825
...
...
EFFECTIVENESS DATE:		20210825
```


2. Filer business metadata

Always present
```
FILER:

    COMPANY DATA:
        ...
    FILING VALUES:
        ...
    BUSINESS ADDRESS:
        ...
    MAIL ADDRESS:
        ...
    FORMER COMPANY:
        ...
```


3. Series and class contracts metadata

Not always present
```
<SERIES-AND-CLASSES-CONTRACTS-DATA>
    <EXISTING-SERIES-AND-CLASSES-CONTRACTS>
        <SERIES>
            <OWNER-CIK>...</OWNER-CIK>
            <SERIES-ID>...</SERIES-ID>
            <SERIES-NAME>...</SERIES-NAME>
            <CLASS-CONTRACT>
                <CLASS-CONTRACT-ID>...</CLASS-CONTRACT-ID>
                <CLASS-CONTRACT-NAME>...</CLASS-CONTRACT-NAME>
                <CLASS-CONTRACT-TICKER-SYMBOL>...</CLASS-CONTRACT-TICKER-SYMBOL>
            </CLASS-CONTRACT>
        </SERIES>
        ...
    </EXISTING-SERIES-AND-CLASSES-CONTRACTS>
</SERIES-AND-CLASSES-CONTRACTS-DATA>
```

4. Pre-document/body riff-raff

Have seen HTML, text, or nothing here.


5. Votes text
Format varies, but generally of a form something like:
```
====================                 FUND 1                 ====================
Votes for holdings in company 1
--------------------------------------------------------------------------------
Votes for holdings in company 2
--------------------------------------------------------------------------------
...

====================                 FUND 2                ====================
Votes for holdings in company 1
--------------------------------------------------------------------------------
Votes for holdings in company 2
--------------------------------------------------------------------------------
```
