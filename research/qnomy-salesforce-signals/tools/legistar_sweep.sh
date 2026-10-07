for c in $(cat clients.txt); do
  r=$(curl -s -m 25 "https://webapi.legistar.com/v1/$c/matters?\$filter=substringof('Salesforce',MatterTitle)%20and%20MatterIntroDate%20ge%20datetime'2025-07-01'&\$select=MatterId,MatterFile,MatterTitle,MatterIntroDate,MatterStatusName&\$top=20")
  n=$(echo "$r" | python3 -c "import sys,json
try:
  d=json.load(sys.stdin)
  for m in d: print('$c',m['MatterIntroDate'][:10],m.get('MatterFile'),m['MatterId'],'|',(m['MatterTitle'] or '')[:300].replace('\n',' '))
except Exception as e: pass")
  if [ -n "$n" ]; then echo "$n"; fi
done
