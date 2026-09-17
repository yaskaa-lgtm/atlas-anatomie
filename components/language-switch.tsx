import {LOCALES,LOCALE_ORDER,useI18n} from '@/lib/i18n';

export function LanguageSwitch(){
 const {locale,setLocale,t}=useI18n();
 return <div className="lang-switch" role="group" aria-label={t('language.label')}>
  {LOCALE_ORDER.map(code=><button key={code} type="button" lang={code} className={code===locale?'active':''} aria-pressed={code===locale} title={t('language.switchTo',{language:LOCALES[code].label})} onClick={()=>setLocale(code)}>{code.toUpperCase()}</button>)}
 </div>;
}
