{extends file="layout.tpl"}

{block name="title"}Tea Framework Demo: todo list{$collection->name|escape}{/block} 

{block name="content"}
<div id="header">
	<div class="content">
		<img src="www/images/g1440.png" alt="icon">
	</div>
</div>


<div id="primary">
	<div class="content">
		{if $msg}
		<h3 class="alert">{$msg}</h3>
		{/if}
		<ul>
			<li><a href="http://necronomicorp.com/l-space/">l-space</a></li>
			<li><a href="http://quickdraw.laits.utexas.edu/dase1">dase dev</a></li>
			<li><a href="https://liberalartsits.seework.com/clients">basecamp</a></li>
			<li><a href="http://nytimes.com">nytimes</a></li>
			<li><a href="http://reddit.com/r/programming">reddit</a></li>
			<li><a href="http://news.ycombinator.com">hacker news</a></li>
			<li><a href="http://del.icio.us/network/pkeane">del.icio.us network</a></li>
			<li><a href="http://twitter.com">twitters</a></li>
			<li><a href="https://utdirect.utexas.edu/pntime/">timesheets</a></li>
			<li><a href="http://atompub.org/rfc4287.html">Atom Syndication Format</a></li>
			<li><a href="http://bitworking.org/projects/atom/rfc5023.html">Atom Publishing Protocol</a></li>
			<li><a href="https://postgres.laits.utexas.edu/phppgadmin">pg</a></li>
		</ul>
	</div>
</div>

<div id="secondary">
	<div class="content">
		<ul id="todos">
			{foreach item="todo" from="$todos"}
			<li><a href="{$app_root}todo/{$todo->id}" class="p{$todo->priority}">{$todo->name}</a> <a href="{$app_root}todo/{$todo->id}" class="delete">[X]</a></li>
			{/foreach}
		</ul>
	</div>
</div>

<div id="tertiary">
	<div class="content">
		<form action="todos" method="post">

			<fieldset>
				<legend>new to do</legend>
				<input type="text" name="name" id="name">
				<!--
				<label for="description">description</label>
				<input type="text" name="description" id="decription">
				-->
				<label for="p1">asap</label>
				<input type="radio" id="p1" name="priority" value="1">
				<label for="p2">soon</label>
				<input type="radio" id="p2" name="priority" value="2" checked>
				<label for="p3">sometime</label>
				<input type="radio" id="p3" name="priority" value="3">
			</fieldset>
			<p>
			<input type="submit" value="add">
			</p>
		</form>
	</div>
</div>
<div id="footer">
	<div class="content">
	</div>
</div>
{/block}
